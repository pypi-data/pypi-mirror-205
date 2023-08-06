"""这是一个封装BLE客户端接口的模块。
它依赖软件包 bleak。
"""

import time
import argparse
import asyncio
import logging
import json

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

class BLEWrapper(object):
    """Note
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._write_wifi_info_uuid = '0000fee3-0000-1000-8000-00805f9b34fb'
        self._notify_wifi_result_uuid = '0000fee4-0000-1000-8000-00805f9b34fb'

    async def write_wifi_info(self, name, address, ssid, password):

        if name:
            device = await BleakScanner.find_device_by_name(
                name, cb=dict(use_bdaddr=False)
            )
            if device is None:
                self._logger.error("could not find device with name '%s'", name)
                return False
        else:
            device = await BleakScanner.find_device_by_address(
                address, cb=dict(use_bdaddr=False)
            )
            if device is None:
                self._logger.error("could not find device with address '%s'", address)
                return False

        self._logger.info("connecting to device...")

        async with BleakClient(device) as client:
            self._logger.info("connected")
            
            data = {}
            data['cmd'] = 1
            data['data'] = {}
            data['data']['ssid'] = ssid
            data['data']['pwd'] = password
            data['data']['label'] = 1

            data_bytes = bytearray(json.dumps(data), encoding='utf-8')
            self._logger.debug("%r", data_bytes)

            try:
                await client.write_gatt_char(self._write_wifi_info_uuid, data_bytes)
                await asyncio.sleep(1.0)
            except Exception as e:
                self._logger.error("write_wifi_info_uuid:%s error:%s", self._write_wifi_info_uuid, e)

            ret = False

            try:
                def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
                    """Simple notification handler which prints the data received."""
                    self._logger.info("%s: %r", characteristic.description, data)
                    if characteristic.uuid == self._notify_wifi_result_uuid and json.loads(str(data, encoding='utf-8'))['code'] == 0:
                        ret = True    

                await client.start_notify(self._notify_wifi_result_uuid, notification_handler)
                await asyncio.sleep(5.0)
                await client.stop_notify(self._notify_wifi_result_uuid)
            except Exception as e:
                self._logger.error("notify_wifi_result_uuid:%s error:%s", self._notify_wifi_result_uuid, e)
        
        return ret

    async def connect(self, name, address):

        if name:
            device = await BleakScanner.find_device_by_name(
                name, cb=dict(use_bdaddr=False)
            )
            if device is None:
                self._logger.error("could not find device with name '%s'", name)
                return False
        else:
            device = await BleakScanner.find_device_by_address(
                address, cb=dict(use_bdaddr=False)
            )
            if device is None:
                self._logger.error("could not find device with address '%s'", address)
                return False

        return True
    
    def config_wifi_info(self, name, address, ssid, password):
        ret = asyncio.run(self.write_wifi_info(name, address, ssid, password))
        self._logger.info("write_wifi_info ret:%d", ret)
        return ret

    def do_connect(self, name, address):
        ret = asyncio.run(self.connect(name, address))
        self._logger.info("connect ret:%d", ret)
        return ret

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    name =  'EM-0123-0001'
    address = None
    
    ble = BLEWrapper()
    ble.do_connect(name, address)