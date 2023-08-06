import asyncio
import logging

import pyshark as pyshark
from pyshark.packet.packet import Packet

from roborock.containers import HomeDataDevice, NetworkInfo
from roborock.containers import RoborockLocalDeviceInfo
from roborock.local_api import RoborockLocalClient
from roborock.roborock_message import RoborockParser, RoborockMessage
from roborock.typing import CommandInfo, RoborockCommand

local_ip = "192.168.1.33"
local_key = "nXTBj42ej5WxQopO"
device_id = "1r9W0cAmDZ2COuVekgRhKa"

buffer = {0: bytes()}


class MyProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        ip, port = addr
        local_device_info = RoborockLocalDeviceInfo(
            device=HomeDataDevice(duid=device_id, local_key=local_key, name="test name", fv="1"),
            network_info=NetworkInfo(ip=local_ip),
        )
        client = RoborockLocalClient(local_device_info)
        asyncio.ensure_future(client.send_message(RoborockMessage(protocol=0, payload=b""))).add_done_callback(
            lambda status: print(status.result())
        )


async def main():
    logging_config = {"level": logging.DEBUG}
    logging.basicConfig(**logging_config)

    # loop = asyncio.get_event_loop()
    # transport, protocol = await loop.create_datagram_endpoint(
    #     MyProtocol,
    #     local_addr=('0.0.0.0', 58866)
    # )
    # await asyncio.sleep(10000)
    #
    local_device_info1 = RoborockLocalDeviceInfo(
        device=HomeDataDevice(duid=device_id, local_key=local_key, name="test name", fv="1"),
        network_info=NetworkInfo(ip=local_ip),
    )
    client1 = RoborockLocalClient(local_device_info1)
    status = await client1.send_command(RoborockCommand.APP_STOP)
    print(status)
    capture = pyshark.LiveCapture(interface="rvi0")

    def on_package(packet: Packet):
        if hasattr(packet, "ip"):
            if packet.transport_layer == "TCP" and (packet.ip.dst == local_ip or packet.ip.src == local_ip):
                if hasattr(packet, "DATA"):
                    if hasattr(packet.DATA, "data"):
                        if packet.ip.dst == local_ip:
                            # print("Request")
                            try:
                                f, buffer[0] = RoborockParser.decode(
                                    buffer[0] + bytes.fromhex(packet.DATA.data), local_key
                                )
                                for i in f:
                                    method = i.get_method()
                                    existed = methods.get(method)
                                    methods.update({method: CommandInfo(prefix=i.prefix, params=i.get_params())})
                                    if not existed:
                                        print(methods)
                                # print(f)
                                # print(buffer[0])
                            except BaseException as e:
                                print(e)
                                pass
                        elif packet.ip.src == local_ip:
                            # print("Response")
                            try:
                                f, buffer[0] = RoborockParser.decode(
                                    buffer[0] + bytes.fromhex(packet.DATA.data), local_key
                                )
                                # print(f)
                            except BaseException as e:
                                print(e)
                                pass

    while True:
        try:
            await capture.packets_from_tshark(on_package, close_tshark=False)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())

    # [RoborockMessage(protocol=0, payload=b'', seq=1, prefix=b'\x00\x00\x00\x15', version=b'1.0', random=22, timestamp=1682390468)]

# MultiMapsList(max_multi_map=4, max_bak_map=1, multi_map_count=2, map_info=[MultiMapsListMapInfo(mapFlag=0, add_time=1682188845, length=11, name='Apartamento', bak_maps=[MultiMapsListMapInfoBakMaps(mapflag=None, add_time=1682007156)]), MultiMapsListMapInfo(mapFlag=1, add_time=1682389915, length=0, name='', bak_maps=[MultiMapsListMapInfoBakMaps(mapflag=None, add_time=1682389915)])])
# MultiMapsList(max_multi_map=4, max_bak_map=1, multi_map_count=2, map_info=[MultiMapsListMapInfo(mapFlag=0, add_time=1682188845, length=11, name='Apartamento', bak_maps=[MultiMapsListMapInfoBakMaps(mapflag=None, add_time=1682007156)]), MultiMapsListMapInfo(mapFlag=1, add_time=1682389915, length=0, name='', bak_maps=[MultiMapsListMapInfoBakMaps(mapflag=None, add_time=1682389915)])])
