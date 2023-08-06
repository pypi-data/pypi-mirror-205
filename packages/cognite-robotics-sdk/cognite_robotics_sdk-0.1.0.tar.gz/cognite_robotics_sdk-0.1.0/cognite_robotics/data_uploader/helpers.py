# -*- coding: utf-8 -*-
"""Data uploader helpers."""
import asyncio
import glob
import json
import logging
import os
import re
import shutil
from collections import defaultdict
from typing import Any, Dict, List, MutableMapping, Optional, Union

import aiofiles
import aiofiles.os
import pydantic
from data_classes import JSONRPCRequest

from cognite_robotics.data_uploader.data_classes import (
    Datapoint,
    DatapointsUploadRequest,
    DataUploaderConfig,
    FileUploadRequest,
    UploadRequestParseError,
)
from cognite_robotics.protos.messages import common_pb2, data_pb2

logger = logging.getLogger(__name__)


async def create_file_upload_request(
    file_path: str,
    data_type: str,
    mission_id: str,
    mission_run_id: str,
    action_run_id: str,
    data_capture_time: int,
    filename_prefix: Optional[str],
    config: DataUploaderConfig,
    data_set_id: int,
    cdf_metadata: Dict[str, Any] = {},
    asset_ids: Optional[List[int]] = None,
    upload_instructions: Optional[JSONRPCRequest] = None,
    data_postprocessing_input: Optional[JSONRPCRequest] = None,
) -> None:
    """Parse data for file upload."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File path does not exist: `{file_path}`.")

    name = _create_cdf_filename(
        filename_prefix=filename_prefix,
        mission_run_id=mission_run_id,
        action_run_id=action_run_id,
        data_type=data_type,
        timestamp=data_capture_time,
    )

    external_id = name

    upload_data_path = config.upload_data_path
    if not os.path.exists(upload_data_path):
        os.makedirs(upload_data_path, exist_ok=True)

    file_extension = os.path.splitext(file_path)[1]
    if file_extension.lower() == ".jpeg":
        os.rename(file_path, file_path.replace(".jpeg", ".jpg"))

    upload_file_path = os.path.join(upload_data_path, name + file_extension)

    cdf_metadata.update(
        {
            "mission_id": mission_id,
            "mission_run_id": mission_run_id,
            "action_run_id": action_run_id,
        }
    )

    asset_id = asset_ids[0] if asset_ids is not None and len(asset_ids) > 0 else None
    if asset_id is not None:
        cdf_metadata.update({"asset_id": asset_id})

    upload_request = FileUploadRequest(
        name=name,
        mission_run_id=mission_run_id,
        mission_id=mission_id,
        action_run_id=action_run_id,
        timestamp_ms=data_capture_time,
        data_set_id=data_set_id,
        upload_instructions=upload_instructions,
        data_postprocessing_input=data_postprocessing_input,
        asset_ids=asset_ids,
        cdf_metadata=cdf_metadata,
        file_path=os.path.abspath(upload_file_path),
        external_id=external_id,
    )

    try:
        await asyncio.shield(aiofiles.os.rename(file_path, upload_file_path))
    except Exception as e:
        logger.info("Failed to copy file to upload data path.")
        # clean up of data file (if exists)
        await remove_files([upload_file_path])
        raise e

    try:
        await _create_upload_request_json(upload_request=upload_request, config=config)
    except Exception as e:
        logger.info("Failed to create upload request json.")
        # clean up of both json and associated data files (if exists)
        await remove_files(glob.glob(os.path.join(config.upload_data_path, f"{name}.*")))
        raise e


async def create_datapoints_upload_request(
    measurements: List[Union[str, float]],
    timestamps: List[int],
    data_type: str,
    timeseries_external_id: str,
    mission_id: str,
    mission_run_id: str,
    action_run_id: str,
    config: DataUploaderConfig,
    data_set_id: int,
    cdf_metadata: Optional[Dict[str, Any]] = None,
    asset_ids: Optional[List[int]] = None,
    upload_instructions: Optional[JSONRPCRequest] = None,
    data_postprocessing_input: Optional[JSONRPCRequest] = None,
) -> None:
    """Process a measurement (float or string)."""
    if len(measurements) == 0:
        logger.info("No measurements to upload.")
        return
    if len(timestamps) == 1:
        timestamps = [timestamps[0]] * len(measurements)
    elif len(measurements) != len(timestamps):
        raise ValueError(f"Number of measurements ({len(measurements)}) and timestamps ({len(timestamps)}) must be equal.")

    datapoints = [Datapoint(timestamp=timestamp, value=measurement) for timestamp, measurement in zip(timestamps, measurements)]

    name = _create_cdf_filename(mission_run_id=mission_run_id, action_run_id=action_run_id, data_type=data_type, timestamp=timestamps[0])

    upload_request = DatapointsUploadRequest(
        name=name,
        mission_id=mission_id,
        mission_run_id=mission_run_id,
        action_run_id=action_run_id,
        timestamp_ms=timestamps[0],
        data_set_id=data_set_id,
        upload_instructions=upload_instructions,
        data_postprocessing_input=data_postprocessing_input,
        asset_ids=asset_ids,
        cdf_metadata=cdf_metadata,
        datapoints=datapoints,
        timeseries_external_id=timeseries_external_id,
    )

    await _create_upload_request_json(upload_request=upload_request, config=config)


async def _create_upload_request_json(
    upload_request: Union[FileUploadRequest, DatapointsUploadRequest], config: DataUploaderConfig
) -> None:
    """Create a JSON file containing the upload request data."""

    async def _create() -> None:
        filename_json = upload_request.name + ".json"
        file_path_raw = os.path.join(config.raw_data_path, filename_json)

        try:
            async with aiofiles.open(file_path_raw, mode="w") as f:
                await f.write(json.dumps(upload_request.dict(), indent=4))
        except Exception as e:
            raise e

        os.rename(file_path_raw, os.path.join(config.upload_data_path, filename_json))

    await asyncio.shield(_create())


async def get_upload_request_from_json(upload_request_json_filename: str) -> Union[FileUploadRequest, DatapointsUploadRequest]:
    """Create UploadInfo from JSON file."""
    async with aiofiles.open(upload_request_json_filename) as json_file:
        contents = await json_file.read()
    data = json.loads(contents)

    if "file_path" in data:
        return pydantic.tools.parse_obj_as(FileUploadRequest, data)
    elif "datapoints" in data:
        return pydantic.tools.parse_obj_as(DatapointsUploadRequest, data)
    else:
        raise UploadRequestParseError(data)


def create_data_upload_event_message(upload_request: Union[FileUploadRequest, DatapointsUploadRequest]) -> data_pb2.DataUploadEvent:
    """Create data upload event message."""
    data_upload_message = data_pb2.DataUploadEvent(
        mission_report_id=upload_request.mission_run_id,
        action_report_id=upload_request.action_run_id,
        data_capture_time=upload_request.timestamp_ms,
        data_postprocessing_input=json.dumps(upload_request.data_postprocessing_input.dict())
        if upload_request.data_postprocessing_input is not None
        else "",
    )
    if upload_request.asset_ids is not None:
        data_upload_message.asset_ids.extend(upload_request.asset_ids)
    return data_upload_message


def create_data_upload_error_message(
    error: Exception,
    upload_request: Union[FileUploadRequest, DatapointsUploadRequest],
) -> data_pb2.DataUploadEvent:
    """Create data upload error message."""
    data_upload_message = create_data_upload_event_message(upload_request=upload_request)
    error_message = common_pb2.ErrorMessage(message=str(error))
    data_upload_message.error_message.CopyFrom(error_message)
    return data_upload_message


def _create_cdf_filename(
    mission_run_id: str, action_run_id: str, data_type: str, timestamp: int, filename_prefix: Optional[str] = None
) -> str:
    """Create a name for the file to be uploaded."""
    if filename_prefix is not None:
        name = "_".join([filename_prefix, data_type, mission_run_id, action_run_id])
    else:
        name = "_".join([data_type, mission_run_id, action_run_id])

    # to avoid duplicate file names, append the data capture time to the end of the file name (if not already present)
    if re.search(r"\d+$", name) is None:
        name = f"{name}_{timestamp}"

    name = name.replace(".", "_")

    return name


async def remove_files(files: List[str]) -> None:
    """Remove files."""

    def _remove_files() -> None:
        for file in files:
            if not os.path.exists(file):
                logger.debug(f"File `{file}` does not exist. Skipping removal.")
                continue
            try:
                os.remove(file)
                logger.debug(f"Removed {file}.")
            except OSError as e:
                logger.error(f"Failed to remove `{file}`: {str(e)}")

    await asyncio.shield(asyncio.to_thread(_remove_files))


async def move_files(
    files: List[str],
    to_folder: str,
) -> None:
    """Move files."""

    def _move_files() -> None:
        for file in files:
            if not os.path.exists(file):
                logger.debug(f"File `{file}` does not exist. Skipping moving.")
                continue
            try:
                os.rename(file, os.path.join(to_folder, os.path.basename(file)))
                logger.debug(f"Moved {file} to {to_folder}.")
            except Exception as e:
                logger.error(f"Failed to move `{file}`: {str(e)}")

    await asyncio.shield(asyncio.to_thread(_move_files))


async def cleanup_upload_data_folder(upload_data_path: str) -> None:
    """Clean up the upload data folder.

    List all files in the upload data folder, check if there is a JSON file (e.g., the upload request instructions) for each file.
    If no associated JSON file is found, remove all other files.
    """
    files = [f for f in glob.glob(os.path.join(upload_data_path, "*")) if not f.startswith(".")]

    grouped_files = defaultdict(list)
    for file in files:
        filename, _ = os.path.splitext(file)
        grouped_files[filename].append(file)

    for filename, files in grouped_files.items():
        has_json = any(f for f in files if f.endswith(".json"))
        if not has_json:
            logger.info(f"Removing files without JSON: {files}")
            await remove_files(files)


async def cleanup_folder(folder: str) -> None:
    """Clean up a folder.

    List all files in the folder, remove all files and subdirectories
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                await asyncio.shield(asyncio.to_thread(shutil.rmtree, file_path))
        except Exception as e:
            logger.error(f"Failed to delete {file_path}: {e}")


def flatten_dict(d: Union[Dict[Any, Any], MutableMapping[Any, Any]], parent_key: str = "", sep: str = "_") -> Dict[Any, Any]:
    """Flatten dictionary.

    Args:
        d (Union[Dict[Any, Any], MutableMapping[Any, Any]]): dictionary to be flattened
        parent_key (str, optional): parent key. Defaults to "".
        sep (str, optional): seperator for the keys when flattening. Defaults to "_".

    Returns:
        Dict[Any, Any]: Flattened dictionary
    """
    items: List[Any] = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
