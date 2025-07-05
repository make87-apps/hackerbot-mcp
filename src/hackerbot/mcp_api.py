# fastmcp decorator-based API for Hackerbot
from typing import Optional, List, TypedDict, Union, Literal

import fastmcp
from hackerbot import Hackerbot

# Instantiate MCP app and Hackerbot
mcp = fastmcp.FastMCP()
hb = Hackerbot()


@mcp.resource(
    "maps://list",
    description="""
        Returns a list of all available map IDs.

        - Checks system readiness before requesting the list.
        - On success: returns a list of strings (map IDs).
        - On error: logs the error and returns None.
    """,
)
def maps_list() -> Optional[List[str]]:
    return hb.base.maps.list()


class PositionDict(TypedDict):
    x: float
    y: float
    angle: float


@mcp.resource(
    "maps://position",
    description="""
        Returns the current position of the base on the map as a dict:
        - x (float): X coordinate (meters)
        - y (float): Y coordinate (meters)
        - yaw (float): Heading angle (degrees)
    """,
)
def maps_position() -> Union[PositionDict, Literal[False]]:
    return hb.base.maps.position()


@mcp.resource(
    "maps://{map_id}",
    description="""
        Fetches map data for the given map ID.

        - Checks system readiness before requesting.
        - On success: returns compressed map data as a string.
        - On error: logs the error and returns None.

        Args:
            map_id (str): The ID of the map to fetch.
    """,
)
def maps_fetch(map_id: str) -> Optional[str]:
    return hb.base.maps.fetch(map_id)


class BaseStatusDict(TypedDict):
    timestamp: Optional[str]  # or str/int, depending on actual data
    left_encoder: Optional[str]  # or int, depending on your data
    right_encoder: Optional[str]
    left_speed: Optional[str]
    right_speed: Optional[str]
    left_set_speed: Optional[str]
    right_set_speed: Optional[str]
    wall_tof: Optional[str]


@mcp.resource(
    "base://status",
    description="""
        Returns the current status of the base as a dictionary with these keys:
        - timestamp
        - left_encoder
        - right_encoder
        - left_speed
        - right_speed
        - left_set_speed
        - right_set_speed
        - wall_tof
    """,
)
def base_status() -> Optional[BaseStatusDict]:
    return hb.base.status()


@mcp.tool(
    "maps/goto",
    description="""
        Commands the robot to move to a specified location on the map.

        Args:
            x (float): X coordinate in meters.
            y (float): Y coordinate in meters.
            angle (float): Heading angle in degrees.
            speed (float): Movement speed in meters per second.
            block (bool, optional): If True, waits until arrival. Default is True.

        Returns:
            bool: True if command succeeded, False if an error occurred.
    """,
)
def maps_goto(
    x: float, y: float, angle: float, speed: float, block: bool = True
) -> bool:
    return hb.base.maps.goto(x, y, angle, speed, block)


@mcp.tool(
    "base/set_mode",
    description="""
        Sets the mode of the base.

        Args:
            mode (int): Target mode value.
    """,
)
def base_set_mode(mode: int) -> bool:
    return hb.base.set_mode(mode)


@mcp.tool(
    "base/start",
    description="""
        Starts the base.

        Args:
            block (bool, optional): If True, blocks until complete. Default is True.

        Returns:
            bool: True if start command succeeded, False otherwise.
    """,
)
def base_start(block: bool = True) -> bool:
    return hb.base.start(block)


@mcp.tool(
    "base/quickmap",
    description="""
        Starts the quick mapping process.

        Args:
            block (bool, optional): If True, blocks until complete. Default is True.

        Returns:
            bool: True if mapping succeeded, False otherwise.
    """,
)
def base_quickmap(block: bool = True) -> bool:
    return hb.base.quickmap(block)


@mcp.tool(
    "base/dock",
    description="""
        Commands the base to dock at the docking station.

        Args:
            block (bool, optional): If True, blocks until complete. Default is True.

        Returns:
            bool: True if docking succeeded, False otherwise.
    """,
)
def base_dock(block: bool = True) -> bool:
    return hb.base.dock(block)


@mcp.tool(
    "base/kill",
    description="""
        Stops all movement immediately (blocking call).

        - After calling, base cannot move until base/start is called.
    """,
)
def base_kill() -> bool:
    return hb.base.kill()


@mcp.tool(
    "base/trigger_bump",
    description="""
        Activates or deactivates bump sensors.

        Args:
            left (int): 1 to enable, 0 to disable left bump sensor.
            right (int): 1 to enable, 0 to disable right bump sensor.

        Returns:
            bool: True if command succeeded, False if it failed.
    """,
)
def base_trigger_bump(left: int, right: int) -> bool:
    return hb.base.trigger_bump(left, right)


@mcp.tool(
    "base/drive",
    description="""
        Sets the base velocity.

        Args:
            l_vel (int): Linear velocity in mm/s (positive = forward, negative = backward).
            a_vel (int): Angular velocity in degrees/s (positive = CCW, negative = CW).
            block (bool, optional): If True, blocks until movement complete.

        Returns:
            bool: True if command succeeded, False otherwise.
    """,
)
def base_drive(l_vel: int, a_vel: int, block: bool = True) -> bool:
    return hb.base.drive(l_vel, a_vel, block)


@mcp.tool(
    "base/destroy",
    description="""
        Stops and shuts down the base. Optionally docks first.

        Args:
            auto_dock (bool, optional): If True, dock before shutdown. Default is False.

        Returns:
            bool: True if shutdown succeeded, False otherwise.
    """,
)
def base_destroy(auto_dock: bool = False) -> None:
    return hb.base.destroy(auto_dock)


@mcp.tool(
    "base/speak",
    description="""
        Synthesizes and plays speech audio from text.

        Args:
            model_src (str): Path or URL of the voice model.
            text (str): Text to synthesize.
            speaker_id (int, optional): Speaker voice ID.

        Returns:
            bool: True if speech was played, False if an error occurred.
    """,
)
def base_speak(model_src: str, text: str, speaker_id: int = None) -> None:
    return hb.base.speak(model_src, text, speaker_id)


@mcp.tool(
    "head/look",
    description="""
        Moves the head to the specified yaw, pitch, and speed.

        Args:
            yaw (float): Degrees (100.0–260.0).
            pitch (float): Degrees (150.0–250.0).
            speed (int): Speed (6=slow, 70=fast).

        Returns:
            bool: True if movement succeeded, False otherwise.
    """,
)
def head_look(yaw: float, pitch: float, speed: int) -> bool:
    return hb.head.look(yaw, pitch, speed)


@mcp.tool(
    "head/set_idle_mode",
    description="""
        Enables or disables head idle mode.

        Args:
            mode (bool): True to enable idle mode, False to disable.

        Returns:
            bool: True if idle mode was set, False otherwise.
    """,
)
def head_set_idle_mode(mode: bool) -> bool:
    return hb.head.set_idle_mode(mode)


@mcp.tool(
    "head/eyes/gaze",
    description="""
        Moves eyes to specified position in the view.

        Args:
            x (float): X position [-1.0, 1.0].
            y (float): Y position [-1.0, 1.0].

        Returns:
            bool: True if movement succeeded, False otherwise.
    """,
)
def eyes_gaze(x: float, y: float) -> bool:
    return hb.head.eyes.gaze(x, y)


@mcp.tool(
    "/arm/move_joint",
    description="""
        Moves a single joint of the arm.

        Args:
            joint_id (int): Joint number (1–6; 1 is base).
            angle (float): Joint angle (joints 1–5: -165.0–165.0°, joint 6: -175.0–175.0°).
            speed (int): Speed (0–100).

        Returns:
            bool: True if move succeeded, False otherwise.
    """,
)
def arm_move_joint(joint_id: int, angle: float, speed: int) -> bool:
    return hb.arm.move_joint(joint_id, angle, speed)


@mcp.tool(
    "/arm/move_joints",
    description="""
        Moves all six arm joints at once.

        Args:
            j_agl_1 to j_agl_5 (float): Angles for joints 1–5 (-165.0–165.0°).
            j_agl_6 (float): Angle for joint 6 (-175.0–175.0°).
            speed (int): Speed (0–100).

        Returns:
            bool: True if move succeeded, False otherwise.
    """,
)
def arm_move_joints(
    j_agl_1: float,
    j_agl_2: float,
    j_agl_3: float,
    j_agl_4: float,
    j_agl_5: float,
    j_agl_6: float,
    speed: int,
) -> bool:
    return hb.arm.move_joints(
        j_agl_1, j_agl_2, j_agl_3, j_agl_4, j_agl_5, j_agl_6, speed
    )


@mcp.tool(
    "/arm/gripper/calibrate",
    description="""
        Calibrates the gripper.

        Returns:
            bool: True if calibration succeeded, False otherwise.
    """,
)
def gripper_calibrate() -> bool:
    return hb.arm.gripper.calibrate()


@mcp.tool(
    "/arm/gripper/open",
    description="""
        Opens the gripper.

        Returns:
            bool: True if open command succeeded, False otherwise.
    """,
)
def gripper_open() -> bool:
    return hb.arm.gripper.open()


@mcp.tool(
    "/arm/gripper/close",
    description="""
        Closes the gripper.

        Returns:
            bool: True if close command succeeded, False otherwise.
    """,
)
def gripper_close() -> bool:
    return hb.arm.gripper.close()


def start_mcp_server(host: str = "0.0.0.0", port: int = 8000, **kwargs):
    mcp.run(transport="http", host=host, port=port, **kwargs)