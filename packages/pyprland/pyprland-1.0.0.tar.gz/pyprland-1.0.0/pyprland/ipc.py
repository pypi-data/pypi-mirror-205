#!/bin/env python
import asyncio
from typing import Any
import json
import os

from .common import DEBUG


HYPRCTL = f'/tmp/hypr/{ os.environ["HYPRLAND_INSTANCE_SIGNATURE"] }/.socket.sock'
EVENTS = f'/tmp/hypr/{ os.environ["HYPRLAND_INSTANCE_SIGNATURE"] }/.socket2.sock'


async def get_event_stream():
    return await asyncio.open_unix_connection(EVENTS)


async def hyprctlJSON(command) -> list[dict[str, Any]] | dict[str, Any]:
    if DEBUG:
        print("(JS)>>>", command)
    ctl_reader, ctl_writer = await asyncio.open_unix_connection(HYPRCTL)
    ctl_writer.write(f"-j/{command}".encode())
    await ctl_writer.drain()
    resp = await ctl_reader.read()
    ctl_writer.close()
    await ctl_writer.wait_closed()
    return json.loads(resp)


async def hyprctl(command):
    if DEBUG:
        print(">>>", command)
    ctl_reader, ctl_writer = await asyncio.open_unix_connection(HYPRCTL)
    ctl_writer.write(f"/dispatch {command}".encode())
    await ctl_writer.drain()
    resp = await ctl_reader.read(100)
    ctl_writer.close()
    await ctl_writer.wait_closed()
    if DEBUG:
        print("<<<", resp)
    return resp == b"ok"


async def get_workspaces() -> list[dict[str, Any]]:
    return await hyprctlJSON("workspaces")


async def get_focused_monitor_props():
    for monitor in await hyprctlJSON("monitors"):
        assert isinstance(monitor, dict)
        if monitor.get("focused") == True:
            return monitor


async def get_client_props_by_pid(pid: int):
    for client in await hyprctlJSON("clients"):
        if client.get("pid") == pid:
            return client
