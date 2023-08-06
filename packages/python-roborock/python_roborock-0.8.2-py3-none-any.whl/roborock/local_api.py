from __future__ import annotations

import asyncio
import logging
import socket
from asyncio import Lock, Transport
from typing import Optional

import async_timeout

from roborock.util import get_running_loop_or_create_one
from .api import QUEUE_TIMEOUT, SPECIAL_COMMANDS, RoborockClient
from .containers import RoborockLocalDeviceInfo
from .exceptions import CommandVacuumError, RoborockConnectionException, RoborockException
from .roborock_message import RoborockMessage, RoborockParser
from .typing import CommandInfoMap, RoborockCommand

_LOGGER = logging.getLogger(__name__)


class RoborockLocalClient(RoborockClient, asyncio.Protocol):
    def __init__(self, device_info: RoborockLocalDeviceInfo):
        super().__init__("abc", device_info)
        self.loop = get_running_loop_or_create_one()
        self.ip = device_info.network_info.ip
        self._batch_structs: list[RoborockMessage] = []
        self._executing = False
        self.remaining = b""
        self.transport: Transport | None = None
        self._mutex = Lock()

    def data_received(self, message):
        if self.remaining:
            message = self.remaining + message
            self.remaining = b""
        (parser_msg, remaining) = RoborockParser.decode(message, self.device_info.device.local_key)
        self.remaining = remaining
        self.on_message(parser_msg)

    def connection_lost(self, exc: Optional[Exception]):
        self.on_disconnect(exc)

    def is_connected(self):
        return self.transport and self.transport.is_reading()

    async def async_connect(self) -> None:
        try:
            if not self.is_connected():
                async with async_timeout.timeout(QUEUE_TIMEOUT):
                    _LOGGER.info(f"Connecting to {self.ip}")
                    self.transport, _ = await self.loop.create_connection(lambda: self, self.ip, 58867)  # type: ignore
        except Exception as e:
            raise RoborockConnectionException(f"Failed connecting to {self.ip}") from e

    async def async_disconnect(self) -> None:
        if self.transport:
            self.transport.close()

    def build_roborock_message(self, method: RoborockCommand, params: Optional[list] = None) -> RoborockMessage:
        secured = True if method in SPECIAL_COMMANDS else False
        request_id, timestamp, payload = self._get_payload(method, params, secured)
        _LOGGER.debug(f"id={request_id} Requesting method {method} with {params}")
        command_info = CommandInfoMap.get(method)
        if not command_info:
            raise RoborockException(f"Request {method} have unknown prefix. Can't execute in offline mode")
        command = CommandInfoMap.get(method)
        if command is None:
            raise RoborockException(f"No prefix found for {method}")
        prefix = command.prefix
        request_protocol = 4
        return RoborockMessage(
            prefix=prefix,
            timestamp=timestamp,
            protocol=request_protocol,
            payload=payload,
        )

    async def send_command(self, method: RoborockCommand, params: Optional[list] = None):
        roborock_message = self.build_roborock_message(method, params)
        return (await self.send_message(roborock_message))[0]

    async def async_local_response(self, roborock_message: RoborockMessage):
        request_id = roborock_message.get_request_id()
        if request_id is not None:
            # response_protocol = 5 if roborock_message.prefix == secured_prefix else 4
            response_protocol = 4
            (response, err) = await self._async_response(request_id, response_protocol)
            if err:
                raise CommandVacuumError("", err) from err
            _LOGGER.debug(f"id={request_id} Response from {roborock_message.get_method()}: {response}")
            return response

    def _send_msg_raw(self, data: bytes):
        try:
            if not self.transport:
                raise RoborockException("Can not send message without connection")
            self.transport.write(data)
        except Exception as e:
            raise RoborockException(e) from e

    async def send_message(self, roborock_messages: list[RoborockMessage] | RoborockMessage):
        async with self._mutex:
            await self.async_connect()
            if isinstance(roborock_messages, RoborockMessage):
                roborock_messages = [roborock_messages]
            local_key = self.device_info.device.local_key
            msg = RoborockParser.encode(roborock_messages, local_key)
            # Send the command to the Roborock device
            if not self.should_keepalive():
                await self.async_disconnect()

            _LOGGER.debug(f"Requesting device with {roborock_messages}")
            self._send_msg_raw(msg)

            responses = await asyncio.gather(
                *[self.async_local_response(roborock_message) for roborock_message in roborock_messages],
                return_exceptions=True,
            )
            exception = next((response for response in responses if isinstance(response, BaseException)), None)
            if exception:
                await self.async_disconnect()
                raise exception
            return responses


class RoborockSocket(socket.socket):
    _closed = None

    @property
    def is_closed(self):
        return self._closed
