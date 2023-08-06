# -*- coding: utf-8 -*-
"""Helper functions to create gRPC messages."""


from typing import List

from cognite_robotics.protos.messages.geometry_pb2 import BODY, MAP, Point, Quaternion, Transform
from cognite_robotics.protos.messages.mission_pb2 import RobotCapability
from cognite_robotics.protos.messages.robot_registration_pb2 import Metadata, RobotRegistrationRequest
from cognite_robotics.protos.messages.robot_state_pb2 import RobotState, RobotStateMessage
from cognite_robotics.protos.messages.video_pb2 import CameraControls, VideoComposition, VideoConfiguration


def robot_registration_request(
    robot_name: str,
    robot_description: str,
    robot_type: str,
    robot_capability_external_ids: List[str],
    video_configuration: VideoConfiguration,
    has_estop: bool,
    has_power_on: bool,
) -> RobotRegistrationRequest:
    """Create a RobotRegistrationRequest.

    Args:
        robot_name (str): Name of the robot
        robot_description (str): Description of the robot
        robot_type (str): Type of the robot (e.g. SPOT, TAUROB, ANYMAL etc.)
        robot_capabilities (List[RobotCapability]): List of robot capabilities
        video_configuration (VideoConfiguration): VideoConfiguration object
        has_estop (bool): The robot has an available emergency stop
        has_power_on (bool): The robot has an available power on/off capability
    Returns:
        RobotRegistrationRequest: RobotRegistrationRequest object
    """
    request = RobotRegistrationRequest(robot_name=robot_name, robot_description=robot_description, robot_type=robot_type)
    request.capabilities.extend(
        [RobotCapability(capability_external_id=capability_external_id) for capability_external_id in robot_capability_external_ids]
    )
    metadata = Metadata(
        three_d_model="", # TODO: Deprecate this: https://cognitedata.atlassian.net/browse/RS-1133
        get_estop=has_estop,
        power_on=has_power_on,
    )
    request.video_config.CopyFrom(video_configuration)
    request.metadata.CopyFrom(metadata)
    return request


def video_configuration(
    description: str, stream_id: int, room_id: int, available_video_compositions: List[str], ptz_go_to: bool, navigate_to: bool
) -> VideoConfiguration:
    """Create a VideoConfiguration.

    Args:
        description (str): Description of the video feed
        stream_id (int): ID of the stream
        room_id (int): ID of the room
        available_video_compositions (List[str]): List of available video compositions
        ptz_go_to (bool): The robot supports controlling PTZ camera by clicking in video stream
        navigate_to (bool): he robot supports navigation by clicking in video stream
    Returns:
        VideoConfiguration: VideoConfiguration object
    """
    return VideoConfiguration(
        description=description,
        stream_id=stream_id,
        room_id=room_id,
        available_video_compositions=[VideoComposition(screen=screen) for screen in available_video_compositions],
        available_camera_controls=CameraControls(
            ptz_go_to=ptz_go_to,
            navigate_to=navigate_to,
        ),
    )


def robot_pose_state_message(
    timestamp: int, pos_x: float, pos_y: float, pos_z: float, quat_x: int, quat_y: int, quat_z: int, quat_w: int
) -> RobotStateMessage:
    """Create a RobotStateMessage with the robot pose.

    Args:
        timestamp (int): Timestamp of the state
        pos_x (float): X position of the robot
        pos_y (float): Y position of the robot
        pos_z (float): Z position of the robot
        quat_x (int): X quaternion of the robot
        quat_y (int): Y quaternion of the robot
        quat_z (int): Z quaternion of the robot
        quat_w (int): W quaternion of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    position = Point(x=pos_x, y=pos_y, z=pos_z)
    orientation = Quaternion(x=quat_x, y=quat_y, z=quat_z, w=quat_w)
    transform = Transform(to=MAP, frm=BODY, translation=position, orientation=orientation)
    robot_state = RobotState(map_transform=transform)
    robot_status_message = RobotStateMessage(ping_sent=timestamp)
    robot_status_message.robot_state.CopyFrom(robot_state)
    return robot_status_message


def robot_battery_percentage_state_message(timestamp: int, battery_percentage: float) -> RobotStateMessage:
    """Create a RobotStateMessage with the battery percentage.

    Args:
        timestamp (int): Timestamp of the state
        battery_percentage (float): Battery percentage of the robot
    Returns:
        RobotStateMessage: RobotStateMessage object
    """
    robot_state = RobotState(battery_percentage=battery_percentage)
    robot_status_message = RobotStateMessage(ping_sent=timestamp)
    robot_status_message.robot_state.CopyFrom(robot_state)
    return robot_status_message
