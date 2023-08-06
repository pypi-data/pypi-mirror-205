# -*- coding: utf-8 -*-
"""Utils tests."""
import asyncio
import logging
import os
from typing import AsyncGenerator, List, Optional, TypeVar

import grpc
from cognite.client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def yield_from_queue(queue: asyncio.Queue[T]) -> AsyncGenerator[T, None]:
    """Yield items from a queue.

    Args:
        queue (asyncio.Queue[T]): queue to yield items from
    Returns:
        AsyncGenerator[T, None]: generator of items from the queue
    """
    while True:
        item = await queue.get()
        yield item


async def handle_grpc_error(
    e: grpc.RpcError,
    invoker: Optional[str] = None,
    error_codes_to_handle_silently: List[grpc.StatusCode] = [
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.INTERNAL,
        grpc.StatusCode.UNAUTHENTICATED,
    ],
) -> None:
    """Handle gPRC errors.

    Args:
        e (grpc.RpcError): RpcError to handle
        invoker (Optional[str], optional): Invoker of the gRPC call. Defaults to None.
        error_codes_to_handle_silently (List[grpc.StatusCode], optional): List of error codes to handle silently.

    Raises:
        e: if error is not in error_codes_to_handle_silently
    """
    if e.code() in error_codes_to_handle_silently:
        # grpc channel is not ready, wait a little bit and try to setup a new stream
        logger.warning(
            f"gRPC error (code: `{e.code()}`, details: `{e.details()}`, invoker: `{invoker if invoker is not None else 'unknown'}`)"
        )
        await asyncio.sleep(1.0)
    else:
        logger.exception(f"gRPC error invoked by `{invoker if invoker is not None else 'unknown'}`", exc_info=e)
        raise e


def create_cognite_client(client_name: str) -> CogniteClient:
    """Use env variables to set up CogniteClient.

    Args:
        client_name (str): client name
    Returns:
        CogniteClient: Cognite CDF client
    """
    cluster = os.getenv("COGNITE_CLUSTER", "")
    base_url = f"https://{cluster}.cognitedata.com"
    project = os.getenv("COGNITE_PROJECT")
    if os.getenv("COGNITE_CLIENT_SECRET"):
        logger.info("Found client secrets")
        tenant_id = os.getenv("COGNITE_TENANT_ID", "")
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        client_id = os.getenv("COGNITE_CLIENT_ID", "")
        token_client_secret = os.getenv("COGNITE_CLIENT_SECRET", "")
        token_scopes = [f"{base_url}/.default"]
    else:
        logger.error("No CDF credentials")
        raise  # TODO: use missing env variable exception

    creds = OAuthClientCredentials(token_url=token_url, client_id=client_id, client_secret=token_client_secret, scopes=token_scopes)
    cnf = ClientConfig(client_name=client_name, base_url=base_url, project=str(project), credentials=creds)
    return CogniteClient(cnf)
