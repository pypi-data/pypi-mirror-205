"""GoXLR Utility API: Main"""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Optional

import typer

from ._version import __version__
from .exceptions import (
    BadMessageException,
    ConnectionClosedException,
    ConnectionErrorException,
)
from .logger import setup_logger
from .models.response import Response
from .websocket_client import WebsocketClient

app = typer.Typer()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
websocket_client = WebsocketClient()


def setup_websocket(
    callback: Optional[Callable[[Response], Awaitable[None]]] = None
) -> None:
    """Listen for messages on another thread"""
    try:
        loop.run_until_complete(websocket_client.connect())
        loop.create_task(
            websocket_client.listen(callback),
            name="Websocket Listener",
        )
    except (
        BadMessageException,
        ConnectionClosedException,
        ConnectionErrorException,
    ) as error:
        typer.secho(
            f"Error: {error}",
            fg=typer.colors.RED,
        )
        loop.stop()


async def message_callback(data: Response) -> None:
    """Message callback function"""
    typer.secho(data.json(), fg=typer.colors.GREEN)


@app.command(name="get_status", short_help="Get Status of GoXLR")
def get_status(debug: bool = False) -> None:
    """Get Status of GoXLR"""
    if debug:
        setup_logger("DEBUG")
    setup_websocket()
    try:
        response: Response = loop.run_until_complete(websocket_client.get_status())
    except BadMessageException as error:
        typer.secho(
            f"Failed to get status from GoXLR: {error}",
            fg=typer.colors.RED,
        )
        return
    typer.secho(response.json(), fg=typer.colors.GREEN)


@app.command(name="listen_for_messages", short_help="Listen for messages")
def listen_for_messages(debug: bool = False) -> None:
    """Listen for messages"""
    if debug:
        setup_logger("DEBUG")
    setup_websocket(message_callback)
    typer.secho("Listening for messages...", fg=typer.colors.GREEN)
    loop.run_forever()


@app.command(name="version", short_help="Module Version")
def version() -> None:
    """Module Version"""
    typer.secho(__version__.public(), fg=typer.colors.CYAN)


if __name__ == "__main__":
    app()
    loop.stop()
