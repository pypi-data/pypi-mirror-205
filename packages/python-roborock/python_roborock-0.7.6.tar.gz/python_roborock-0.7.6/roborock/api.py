"""The Roborock api."""

from __future__ import annotations

import asyncio
import base64
import gzip
import hashlib
import hmac
import json
import logging
import math
import secrets
import struct
import time
from random import randint
from typing import Any, Callable, Coroutine, Mapping, Optional

import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from .code_mappings import RoborockDockTypeCode, RoborockEnum
from .containers import (
    CleanRecord,
    CleanSummary,
    Consumable,
    DNDTimer,
    DustCollectionMode,
    HomeData,
    MultiMapsList,
    NetworkInfo,
    RoborockDeviceInfo,
    RoomMapping,
    SmartWashParams,
    Status,
    UserData,
    WashTowelMode,
)
from .exceptions import RoborockException, RoborockTimeout, VacuumError
from .roborock_future import RoborockFuture
from .roborock_message import RoborockMessage
from .typing import DeviceProp, DockSummary, RoborockCommand
from .util import unpack_list

_LOGGER = logging.getLogger(__name__)
QUEUE_TIMEOUT = 4
SPECIAL_COMMANDS = [
    RoborockCommand.GET_MAP_V1,
]


def md5hex(message: str) -> str:
    md5 = hashlib.md5()
    md5.update(message.encode())
    return md5.hexdigest()


class PreparedRequest:
    def __init__(self, base_url: str, base_headers: Optional[dict] = None) -> None:
        self.base_url = base_url
        self.base_headers = base_headers or {}

    async def request(self, method: str, url: str, params=None, data=None, headers=None) -> dict:
        _url = "/".join(s.strip("/") for s in [self.base_url, url])
        _headers = {**self.base_headers, **(headers or {})}
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                _url,
                params=params,
                data=data,
                headers=_headers,
            ) as resp:
                return await resp.json()


class RoborockClient:
    def __init__(self, endpoint: str, devices_info: Mapping[str, RoborockDeviceInfo]) -> None:
        self.devices_info = devices_info
        self._endpoint = endpoint
        self._nonce = secrets.token_bytes(16)
        self._waiting_queue: dict[int, RoborockFuture] = {}
        self._status_listeners: list[Callable[[int, str], None]] = []

    def add_status_listener(self, callback: Callable[[int, str], None]):
        self._status_listeners.append(callback)

    async def async_disconnect(self) -> Any:
        raise NotImplementedError

    def on_message(self, messages: list[RoborockMessage]) -> None:
        try:
            for data in messages:
                protocol = data.protocol
                if protocol == 102 or protocol == 4:
                    payload = json.loads(data.payload.decode())
                    for data_point_number, data_point in payload.get("dps").items():
                        if data_point_number == "102":
                            data_point_response = json.loads(data_point)
                            request_id = data_point_response.get("id")
                            queue = self._waiting_queue.get(request_id)
                            if queue:
                                if queue.protocol == protocol:
                                    error = data_point_response.get("error")
                                    if error:
                                        queue.resolve(
                                            (
                                                None,
                                                VacuumError(
                                                    error.get("code"),
                                                    error.get("message"),
                                                ),
                                            )
                                        )
                                    else:
                                        result = data_point_response.get("result")
                                        if isinstance(result, list) and len(result) == 1:
                                            result = result[0]
                                        queue.resolve((result, None))
                elif protocol == 301:
                    payload = data.payload[0:24]
                    [endpoint, _, request_id, _] = struct.unpack("<15sBH6s", payload)
                    if endpoint.decode().startswith(self._endpoint):
                        iv = bytes(AES.block_size)
                        decipher = AES.new(self._nonce, AES.MODE_CBC, iv)
                        decrypted = unpad(decipher.decrypt(data.payload[24:]), AES.block_size)
                        decrypted = gzip.decompress(decrypted)
                        queue = self._waiting_queue.get(request_id)
                        if queue:
                            if isinstance(decrypted, list):
                                decrypted = decrypted[0]
                            queue.resolve((decrypted, None))
        except Exception as ex:
            _LOGGER.exception(ex)

    async def _async_response(self, request_id: int, protocol_id: int = 0) -> tuple[Any, VacuumError | None]:
        try:
            queue = RoborockFuture(protocol_id)
            self._waiting_queue[request_id] = queue
            (response, err) = await queue.async_get(QUEUE_TIMEOUT)
            return response, err
        except (asyncio.TimeoutError, asyncio.CancelledError):
            raise RoborockTimeout(f"Timeout after {QUEUE_TIMEOUT} seconds waiting for response") from None
        finally:
            del self._waiting_queue[request_id]

    def _get_payload(self, method: RoborockCommand, params: Optional[list] = None, secured=False):
        timestamp = math.floor(time.time())
        request_id = randint(10000, 99999)
        inner = {
            "id": request_id,
            "method": method,
            "params": params or [],
        }
        if secured:
            inner["security"] = {
                "endpoint": self._endpoint,
                "nonce": self._nonce.hex().lower(),
            }
        payload = bytes(
            json.dumps(
                {
                    "dps": {"101": json.dumps(inner, separators=(",", ":"))},
                    "t": timestamp,
                },
                separators=(",", ":"),
            ).encode()
        )
        return request_id, timestamp, payload

    async def send_command(self, device_id: str, method: RoborockCommand, params: Optional[list] = None):
        raise NotImplementedError

    async def get_status(self, device_id: str) -> Status | None:
        status = await self.send_command(device_id, RoborockCommand.GET_STATUS)
        if isinstance(status, dict):
            return Status.from_dict(status)
        return None

    async def get_dnd_timer(self, device_id: str) -> DNDTimer | None:
        try:
            dnd_timer = await self.send_command(device_id, RoborockCommand.GET_DND_TIMER)
            if isinstance(dnd_timer, dict):
                return DNDTimer.from_dict(dnd_timer)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_clean_summary(self, device_id: str) -> CleanSummary | None:
        try:
            clean_summary = await self.send_command(device_id, RoborockCommand.GET_CLEAN_SUMMARY)
            if isinstance(clean_summary, dict):
                return CleanSummary.from_dict(clean_summary)
            elif isinstance(clean_summary, list):
                clean_time, clean_area, clean_count, records = unpack_list(clean_summary, 4)
                return CleanSummary(
                    clean_time=clean_time, clean_area=clean_area, clean_count=clean_count, records=records
                )
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_clean_record(self, device_id: str, record_id: int) -> CleanRecord | None:
        try:
            clean_record = await self.send_command(device_id, RoborockCommand.GET_CLEAN_RECORD, [record_id])
            if isinstance(clean_record, dict):
                return CleanRecord.from_dict(clean_record)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_consumable(self, device_id: str) -> Consumable | None:
        try:
            consumable = await self.send_command(device_id, RoborockCommand.GET_CONSUMABLE)
            if isinstance(consumable, dict):
                return Consumable.from_dict(consumable)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_wash_towel_mode(self, device_id: str) -> WashTowelMode | None:
        try:
            washing_mode = await self.send_command(device_id, RoborockCommand.GET_WASH_TOWEL_MODE)
            if isinstance(washing_mode, dict):
                return WashTowelMode.from_dict(washing_mode)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_dust_collection_mode(self, device_id: str) -> DustCollectionMode | None:
        try:
            dust_collection = await self.send_command(device_id, RoborockCommand.GET_DUST_COLLECTION_MODE)
            if isinstance(dust_collection, dict):
                return DustCollectionMode.from_dict(dust_collection)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_smart_wash_params(self, device_id: str) -> SmartWashParams | None:
        try:
            mop_wash_mode = await self.send_command(device_id, RoborockCommand.GET_SMART_WASH_PARAMS)
            if isinstance(mop_wash_mode, dict):
                return SmartWashParams.from_dict(mop_wash_mode)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_dock_summary(self, device_id: str, dock_type: RoborockEnum) -> DockSummary | None:
        """Gets the status summary from the dock with the methods available for a given dock.

        :param device_id: Device id
        :param dock_type: RoborockDockTypeCode"""
        try:
            commands: list[
                Coroutine[
                    Any,
                    Any,
                    DustCollectionMode | WashTowelMode | SmartWashParams | None,
                ]
            ] = [self.get_dust_collection_mode(device_id)]
            if dock_type == RoborockDockTypeCode["3"]:
                commands += [
                    self.get_wash_towel_mode(device_id),
                    self.get_smart_wash_params(device_id),
                ]
            [dust_collection_mode, wash_towel_mode, smart_wash_params] = unpack_list(
                list(await asyncio.gather(*commands)), 3
            )

            return DockSummary(dust_collection_mode, wash_towel_mode, smart_wash_params)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_prop(self, device_id: str) -> DeviceProp | None:
        [status, dnd_timer, clean_summary, consumable] = await asyncio.gather(
            *[
                self.get_status(device_id),
                self.get_dnd_timer(device_id),
                self.get_clean_summary(device_id),
                self.get_consumable(device_id),
            ]
        )
        last_clean_record = None
        if clean_summary and clean_summary.records and len(clean_summary.records) > 0:
            last_clean_record = await self.get_clean_record(device_id, clean_summary.records[0])
        dock_summary = None
        if status and status.dock_type is not None and status.dock_type != RoborockDockTypeCode["0"]:
            dock_summary = await self.get_dock_summary(device_id, status.dock_type)
        if any([status, dnd_timer, clean_summary, consumable]):
            return DeviceProp(
                status,
                dnd_timer,
                clean_summary,
                consumable,
                last_clean_record,
                dock_summary,
            )
        return None

    async def get_multi_maps_list(self, device_id) -> MultiMapsList | None:
        try:
            multi_maps_list = await self.send_command(device_id, RoborockCommand.GET_MULTI_MAPS_LIST)
            if isinstance(multi_maps_list, dict):
                return MultiMapsList.from_dict(multi_maps_list)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_networking(self, device_id) -> NetworkInfo | None:
        try:
            networking_info = await self.send_command(device_id, RoborockCommand.GET_NETWORK_INFO)
            if isinstance(networking_info, dict):
                return NetworkInfo.from_dict(networking_info)
        except RoborockTimeout as e:
            _LOGGER.error(e)
        return None

    async def get_room_mapping(self, device_id: str) -> list[RoomMapping]:
        """Gets the mapping from segment id -> iot id. Only works on local api."""
        mapping = await self.send_command(device_id, RoborockCommand.GET_ROOM_MAPPING)
        if isinstance(mapping, list):
            return [
                RoomMapping(segment_id=segment_id, iot_id=iot_id)  # type: ignore
                for segment_id, iot_id in [unpack_list(room, 2) for room in mapping]
            ]
        return []


class RoborockApiClient:
    def __init__(self, username: str, base_url=None) -> None:
        """Sample API Client."""
        self._username = username
        self._default_url = "https://euiot.roborock.com"
        self.base_url = base_url
        self._device_identifier = secrets.token_urlsafe(16)

    async def _get_base_url(self) -> str:
        if not self.base_url:
            url_request = PreparedRequest(self._default_url)
            response = await url_request.request(
                "post",
                "/api/v1/getUrlByEmail",
                params={"email": self._username, "needtwostepauth": "false"},
            )
            if response is None:
                raise RoborockException("get url by email returned None")
            if response.get("code") != 200:
                raise RoborockException(response.get("error"))
            response_data = response.get("data")
            if response_data is None:
                raise RoborockException("response does not have 'data'")
            self.base_url = response_data.get("url")
        return self.base_url

    def _get_header_client_id(self):
        md5 = hashlib.md5()
        md5.update(self._username.encode())
        md5.update(self._device_identifier.encode())
        return base64.b64encode(md5.digest()).decode()

    async def request_code(self) -> None:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()
        code_request = PreparedRequest(base_url, {"header_clientid": header_clientid})

        code_response = await code_request.request(
            "post",
            "/api/v1/sendEmailCode",
            params={
                "username": self._username,
                "type": "auth",
            },
        )
        if code_response is None:
            raise RoborockException("Failed to get a response from send email code")
        if code_response.get("code") != 200:
            raise RoborockException(code_response.get("msg"))

    async def pass_login(self, password: str) -> UserData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()

        login_request = PreparedRequest(base_url, {"header_clientid": header_clientid})
        login_response = await login_request.request(
            "post",
            "/api/v1/login",
            params={
                "username": self._username,
                "password": password,
                "needtwostepauth": "false",
            },
        )
        if login_response is None:
            raise RoborockException("Login response is none")
        if login_response.get("code") != 200:
            raise RoborockException(login_response.get("msg"))
        user_data = login_response.get("data")
        if not isinstance(user_data, dict):
            raise RoborockException("Got unexpected data type for user_data")
        return UserData.from_dict(user_data)

    async def code_login(self, code) -> UserData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()

        login_request = PreparedRequest(base_url, {"header_clientid": header_clientid})
        login_response = await login_request.request(
            "post",
            "/api/v1/loginWithCode",
            params={
                "username": self._username,
                "verifycode": code,
                "verifycodetype": "AUTH_EMAIL_CODE",
            },
        )
        if login_response is None:
            raise RoborockException("Login request response is None")
        if login_response.get("code") != 200:
            raise RoborockException(login_response.get("msg"))
        user_data = login_response.get("data")
        if not isinstance(user_data, dict):
            raise RoborockException("Got unexpected data type for user_data")
        return UserData.from_dict(user_data)

    async def get_home_data(self, user_data: UserData) -> HomeData:
        base_url = await self._get_base_url()
        header_clientid = self._get_header_client_id()
        rriot = user_data.rriot
        if rriot is None:
            raise RoborockException("rriot is none")
        home_id_request = PreparedRequest(base_url, {"header_clientid": header_clientid})
        home_id_response = await home_id_request.request(
            "get",
            "/api/v1/getHomeDetail",
            headers={"Authorization": user_data.token},
        )
        if home_id_response is None:
            raise RoborockException("home_id_response is None")
        if home_id_response.get("code") != 200:
            raise RoborockException(home_id_response.get("msg"))

        home_id = home_id_response["data"].get("rrHomeId")
        timestamp = math.floor(time.time())
        nonce = secrets.token_urlsafe(6)
        prestr = ":".join(
            [
                rriot.u,
                rriot.s,
                nonce,
                str(timestamp),
                hashlib.md5(("/user/homes/" + str(home_id)).encode()).hexdigest(),
                "",
                "",
            ]
        )
        mac = base64.b64encode(hmac.new(rriot.h.encode(), prestr.encode(), hashlib.sha256).digest()).decode()
        if rriot.r.a is None:
            raise RoborockException("Missing field 'a' in rriot reference")
        home_request = PreparedRequest(
            rriot.r.a,
            {
                "Authorization": f'Hawk id="{rriot.u}", s="{rriot.s}", ts="{timestamp}", nonce="{nonce}", mac="{mac}"',
            },
        )
        home_response = await home_request.request("get", "/user/homes/" + str(home_id))
        if not home_response.get("success"):
            raise RoborockException(home_response)
        home_data = home_response.get("result")
        if isinstance(home_data, dict):
            return HomeData.from_dict(home_data)
        else:
            raise RoborockException("home_response result was an unexpected type")
