"""GoXLR Utility API: Websocket Client"""
from __future__ import annotations

import asyncio
import socket
from collections.abc import Awaitable, Callable
from typing import Any, Optional

import aiohttp
import async_timeout
from pydantic import ValidationError

from .base import Base
from .const import (
    ACCENT,
    COMMAND_TYPE_SET_BUTTON_COLOURS,
    COMMAND_TYPE_SET_FADER_COLOURS,
    COMMAND_TYPE_SET_SIMPLE_COLOUR,
    DEFAULT_HOST,
    DEFAULT_PORT,
    KEY_DATA,
    KEY_ID,
    KEY_TYPE,
    MODEL_MAP,
    REQUEST_TYPE_COMMAND,
    REQUEST_TYPE_GET_STATUS,
    RESPONSE_TYPE_OK,
    RESPONSE_TYPE_PATCH,
    RESPONSE_TYPE_STATUS,
)
from .exceptions import (
    BadMessageException,
    ConnectionClosedException,
    ConnectionErrorException,
)
from .models.patch import Patch
from .models.request import Request
from .models.response import Response
from .models.status import Status


class WebsocketClient(Base):
    """Websocket Client"""

    def __init__(self) -> None:
        """Initialize Websocket Client"""
        super().__init__()
        self._current_id: int = 1
        self._mixer_serial_number: Optional[str] = None
        self._responses: dict[
            int, tuple[asyncio.Future[Response[Any]], Optional[str]]
        ] = {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._websocket: Optional[aiohttp.ClientWebSocketResponse] = None

    @property
    def connected(self) -> bool:
        """Get connection state."""
        return self._websocket is not None and not self._websocket.closed

    async def disconnect(self) -> None:
        """Disconnect from server"""
        self._logger.info("Disconnecting from WebSocket")
        if self._websocket is not None:
            await self._websocket.close()

    async def connect(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """Connect to server"""
        if session:
            self._session = session
        else:
            self._logger.info("Creating new aiohttp client session")
            self._session = aiohttp.ClientSession()
        url = f"ws://{host}:{port}/api/websocket"
        self._logger.info(
            "Connecting to WebSocket: %s (aiohttp: %s)",
            url,
            aiohttp.__version__,
        )
        try:
            self._websocket = await self._session.ws_connect(url=url, heartbeat=30)
        except (
            aiohttp.WSServerHandshakeError,
            aiohttp.ClientConnectionError,
            socket.gaierror,
        ) as error:
            raise ConnectionErrorException(error) from error
        self._logger.info("Connected to WebSocket")

    async def _send_message(
        self,
        request: Request,
        wait_for_response: bool = True,
        response_type: Optional[str] = None,
    ) -> Response[Any]:
        """Send a message to the WebSocket"""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        self._current_id += 1
        request.id = self._current_id

        future: asyncio.Future[
            Response[Any]
        ] = asyncio.get_running_loop().create_future()
        self._responses[request.id] = future, response_type
        await self._websocket.send_str(request.json())
        self._logger.debug("Sent message: %s", request.json())
        if wait_for_response:
            try:
                async with async_timeout.timeout(10):
                    return await future
            except asyncio.TimeoutError as error:
                raise BadMessageException("Timeout waiting for response") from error
            finally:
                self._responses.pop(request.id)
        return Response[None](
            id=request.id,
            data=None,
            type=None,
        )

    async def get_status(self) -> Status:
        """Get status from GoXLR"""
        self._logger.info("Getting status from GoXLR")
        response: Response[Status] = await self._send_message(
            Request(data=REQUEST_TYPE_GET_STATUS),
            wait_for_response=True,
            response_type=RESPONSE_TYPE_STATUS,
        )
        if response.data is None:
            raise BadMessageException("Message data is missing")
        self._logger.debug("Status: %s", response.data)
        self._mixer_serial_number = next(iter(response.data.mixers.keys()))
        return response.data

    async def set_accent_color(
        self,
        color: str,
    ) -> None:
        """Set accent color"""
        if self._mixer_serial_number is None:
            raise BadMessageException(
                "Mixer serial number is missing. Call get_status to set this."
            )

        self._logger.info(
            "Setting accent color to '%s' for mixer '%s'",
            color,
            self._mixer_serial_number,
        )
        await self._send_message(
            Request(
                data={
                    REQUEST_TYPE_COMMAND: [
                        self._mixer_serial_number,
                        {
                            COMMAND_TYPE_SET_SIMPLE_COLOUR: [
                                ACCENT,
                                color,
                            ],
                        },
                    ]
                }
            ),
            wait_for_response=False,
            response_type=RESPONSE_TYPE_OK,
        )

    async def set_button_color(
        self,
        name: str,
        color_one: str,
        color_two: str,
    ) -> None:
        """Set button color"""
        if self._mixer_serial_number is None:
            raise BadMessageException(
                "Mixer serial number is missing. Call get_status to set this."
            )

        self._logger.info(
            "Setting button '%s' color to '%s' and '%s' for mixer '%s'",
            name,
            color_one,
            color_two,
            self._mixer_serial_number,
        )
        await self._send_message(
            Request(
                data={
                    REQUEST_TYPE_COMMAND: [
                        self._mixer_serial_number,
                        {
                            COMMAND_TYPE_SET_BUTTON_COLOURS: [
                                name,
                                color_one,
                                color_two,
                            ],
                        },
                    ]
                }
            ),
            wait_for_response=False,
            response_type=RESPONSE_TYPE_OK,
        )

    async def set_fader_color(
        self,
        name: str,
        color_top: str,
        color_bottom: str,
    ) -> None:
        """Set fader color"""
        if self._mixer_serial_number is None:
            raise BadMessageException(
                "Mixer serial number is missing. Call get_status to set this."
            )

        self._logger.info(
            "Setting fader '%s' color to '%s' and '%s' for mixer '%s'",
            name,
            color_top,
            color_bottom,
            self._mixer_serial_number,
        )
        await self._send_message(
            Request(
                data={
                    REQUEST_TYPE_COMMAND: [
                        self._mixer_serial_number,
                        {
                            COMMAND_TYPE_SET_FADER_COLOURS: [
                                name,
                                color_top,
                                color_bottom,
                            ],
                        },
                    ]
                }
            ),
            wait_for_response=False,
            response_type=RESPONSE_TYPE_OK,
        )

    async def listen(
        self,
        patch_callback: Optional[Callable[[Response[Patch]], Awaitable[None]]] = None,
    ) -> None:
        """Listen for patches from GoXLR"""

        async def _message_callback(message: dict) -> None:
            """Message callback"""
            self._logger.debug("New message")

            # Get message ID
            message_id = message.get(KEY_ID)

            if (message_data := message.get(KEY_DATA)) is None:
                raise BadMessageException("Message data is missing")

            # Get key of first object in message data
            if (message_type := next(iter(message_data))) is None:
                raise BadMessageException("Message type is missing")

            self._logger.debug("Message ID: %s", message_id)
            self._logger.debug("Message type: %s", message_type)

            # Find model from module
            if (model := MODEL_MAP.get(message_type)) is None:
                self._logger.warning("Unknown model: %s", message_type)
            else:
                response = Response[Any](
                    id=message_id,
                    data=message_data.get(message_type),
                    type=message_type,
                )

                if response.data is None:
                    raise BadMessageException("Message data is missing")

                try:
                    if isinstance(response.data, list):
                        response.data = [model(**item) for item in response.data]
                    else:
                        response.data = model(**response.data)
                except (TypeError, ValidationError) as error:
                    raise BadMessageException(
                        f"Failed to create model '{message_type}' with data:\n{response.data}"
                    ) from error

                self._logger.info(
                    "Response: %s",
                    response.json(
                        include={
                            KEY_ID,
                            KEY_TYPE,
                        },
                        exclude_unset=True,
                    ),
                )

                if message_id is not None:
                    response_tuple = self._responses.get(message_id)
                    if response_tuple is not None:
                        future, response_type = response_tuple
                        if response_type is not None and response_type != message_type:
                            self._logger.info(
                                "Response type '%s' does not match requested type '%s'.",
                                message_type,
                                response_type,
                            )
                        else:
                            try:
                                future.set_result(response)
                            except asyncio.InvalidStateError:
                                self._logger.debug(
                                    "Future already set for response ID: %s",
                                    message_id,
                                )

                if patch_callback is not None and message_type == RESPONSE_TYPE_PATCH:
                    try:
                        for item in response.data:
                            patch_response = Response[Patch](
                                id=response.id,
                                type=response.type,
                                data=item,
                            )
                            self._logger.debug("Patch callback: %s", patch_response)
                            await patch_callback(patch_response)
                    except (TypeError, ValidationError) as error:
                        raise BadMessageException(
                            f"Failed to create model patch response with data:\n{response.data}"
                        ) from error

        await self._listen_for_messages(callback=_message_callback)

    async def _listen_for_messages(
        self,
        callback: Callable[[dict[Any, Any]], Awaitable[None]],
    ) -> None:
        """Listen for messages"""
        if not self.connected:
            raise ConnectionClosedException("Connection is closed")

        self._logger.info("Listen for messages")
        if self._websocket is not None:
            while not self._websocket.closed:
                message = await self.receive_message()
                if isinstance(message, dict):
                    await callback(message)

    async def receive_message(self) -> Optional[dict]:
        """Receive message"""
        if not self.connected or self._websocket is None:
            raise ConnectionClosedException("Connection is closed")

        try:
            message = await self._websocket.receive()
        except RuntimeError:
            return None

        if message.type == aiohttp.WSMsgType.ERROR:
            raise ConnectionErrorException(self._websocket.exception())

        if message.type in (
            aiohttp.WSMsgType.CLOSE,
            aiohttp.WSMsgType.CLOSED,
            aiohttp.WSMsgType.CLOSING,
        ):
            raise ConnectionClosedException("Connection closed to server")

        if message.type == aiohttp.WSMsgType.TEXT:
            message_json = message.json()

            return message_json

        raise BadMessageException(f"Unknown message type: {message.type}")
