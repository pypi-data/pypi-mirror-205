"""
Stuff for interacting with locid devices via bluetooth
"""

import asyncio
import json
from typing import Union, Tuple, Dict, List, AsyncGenerator
import logging
import bleak

from bleak import BleakClient, BleakScanner, BleakGATTCharacteristic
from pprint import pprint

logger = logging.getLogger('locid_ble')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

LOCID_BLE_SERVICE_UUID = 'b940d010-f5f8-466e-aff9-25556b57fe6d'

LOCID_BLE_UUID_CHAR_FIRMWARE_VERSION =    0x0011
LOCID_BLE_UUID_CHAR_DISTANCE =       0xD011
LOCID_BLE_UUID_CHAR_NEAR =           0xD012
LOCID_BLE_UUID_CHAR_FAR =            0xD013
LOCID_BLE_UUID_CHAR_MAC =            0xD014
LOCID_BLE_UUID_CHAR_TIME =           0xD015
LOCID_BLE_UUID_CHAR_ENABLE=          0xD016
LOCID_BLE_UUID_CHAR_LONG =           0xD017
LOCID_BLE_UUID_CHAR_LAT =            0xD018
LOCID_BLE_UUID_CHAR_DOOR =           0xD019
LOCID_BLE_UUID_CHAR_INVERT_DOOR =    0xD020
LOCID_BLE_UUID_CHAR_GROUP_ID =       0xD021
LOCID_BLE_UUID_CHAR_SYSTEM_ID =       0xD022
LOCID_BLE_UUID_CHAR_BEACON_RSSI =     0xD023
LOCID_BLE_UUID_CHAR_APS_CALL =		0xD024
LOCID_BLE_UUID_CHAR_HOST_COMM =		0xD025
LOCID_BLE_UUID_CHAR_DEVICE_META_INFO =		0xD026
LOCID_BLE_UUID_CHAR_NAME =           0xD01F

def locid_char_uuid_128(short):
    hexstr = "%0.4x" % short
    return f"b940{hexstr}-f5f8-466e-aff9-25556b57fe6d"

async def _bleak_client_conn(client: BleakClient, n_retries=5, disconnected_callback=None):
    # connect
    last_err = None
    for attempt in range(n_retries):
        try:
            await client.connect(
                dangerous_use_bleak_cache=True,
                timeout=20,
                disconnected_callback=disconnected_callback
                )
            return client
        except (bleak.exc.BleakError, bleak.exc.BleakDeviceNotFoundError, bleak.exc.BleakDBusError, asyncio.exceptions.TimeoutError) as e:
            logger.error(f"bleak con err: '{e}' ({type(e)})")
            logger.error(f"discovered devs: {BleakScanner.discovered_devices}")
            if attempt < n_retries:
                print("retrying...")
            last_err = e
            await asyncio.sleep(2)
            #client = BleakClient(client.address)

    raise last_err


async def bleak_client_reliable_connect(client_or_addr: Union[BleakClient, str], n_retries=5, disconnected_callback=None) -> BleakClient:
    """
    Helper for getting connected BleakClient instances (using multiple attempts / platform workarounds)
    """

    if not disconnected_callback:
        disconnected_callback = lambda d: print("discon:", d)

    client = None
    if isinstance(client_or_addr, BleakClient):
        client = client_or_addr
        await _bleak_client_conn(client, n_retries, disconnected_callback)

    elif isinstance(client_or_addr, str):
        logging.info(f"Searching for locid device with ble mac: {client_or_addr}")

        for _ in range(3):
            try:
                bledev = await BleakScanner.find_device_by_address(client_or_addr, timeout=5, cb={"use_bdaddr": True})
                print("bledev:", bledev)
                if bledev:
                    client = BleakClient(bledev)

                await _bleak_client_conn(client, n_retries, disconnected_callback)
                return
            except bleak.exc.BleakError as e:
                logging.exception("bleak error (scan/conn)")
                await asyncio.sleep(2)

    else:
        raise BaseException("invalid client arg")

    if client is None:
        raise BaseException(f"Couldn't find client with addr: {client_or_addr}")


BLE_SERVICE_UUID_NORDIC_NUS = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
BLE_CHAR_UUID_NORDIC_NUS_TX = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
BLE_CHAR_UUID_NORDIC_NUS_RX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

class BleakNordicNusError(BaseException):
    pass

class BleakNordicNus(asyncio.StreamReader, asyncio.StreamWriter):

    client: BleakClient
    client_addr: str
    rxbuf: bytearray

    MAX_RXBUF_LEN = 4096

    def __init__(self, client: Union[BleakClient, str]):

        if client is BleakClient:
            self.client = client
            self.client_addr = client.address
        else:
            self.client_addr = client
            self.client = BleakClient(client)

        self.rxbuf = bytearray()
        self.read_future = None

        super().__init__()

    def on_disconnect(self, bleak_dev: BleakClient):
        logger.info(f"DISCONNECT, bleak_dev: {bleak_dev}")

    async def connect(self):
        # if self.client is None:
        #     self.client = await bleak_client_reliable_connect(self.client_addr, disconnected_callback=self.on_disconnect)

        if not self.client.is_connected:
            logging.info(f"connecting bleak client: {self.client}")
            await bleak_client_reliable_connect(self.client)

        try:
            await self.client.start_notify(BLE_CHAR_UUID_NORDIC_NUS_RX, self._on_rx)
        except Exception as ex:
            logger.exception("notifiy rx char")
            logger.error(f"is connected: {self.client.is_connected}")
            await self.client.disconnect()
            raise ex

    @classmethod
    async def open_connection(cls, client_or_addr) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        self = cls(client_or_addr)
        await self.connect()
        return (self, self)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def disconnect(self):
        if self.read_future:
            self.read_future.cancel()
            self.read_future = None

        if self.client.is_connected:
            try:
                await self.client.stop_notify(BLE_CHAR_UUID_NORDIC_NUS_RX)
            except bleak.exc.BleakError:
                logger.warning("stop notify error (probably bleak bug):", exc_info=1)

            await self.client.disconnect()
        else:
            logger.warning("already disconnected")

    async def close(self):
        await self.disconnect()

    async def write(self, data, mtu=200):
        logger.debug(f"write, data: {data}")

        if not self.client.is_connected:
            raise BleakNordicNusError("client not connected. Please call connect() first")

        data_len = len(data)
        chunks = [ data[i:i + mtu] for i in range(0, data_len, mtu) ]

        for chunk in chunks:
            await self.client.write_gatt_char(BLE_CHAR_UUID_NORDIC_NUS_TX, chunk, response=True)

    async def readline(self):
        logger.debug("readline()")

        fut = asyncio.get_running_loop().create_future()
        self.read_future = fut
        await self._refresh_rx()
        return await fut

    async def _refresh_rx(self):
        """Parses rx buffer and calls callbacks/futures for complete commands"""

        if self.read_future:
            end_idx = self.rxbuf.find(b"\n")

            if end_idx >= 0:
                line = self.rxbuf[0:end_idx+1]
                self.rxbuf = self.rxbuf[end_idx+1:]

                self.read_future.set_result(line)
                self.read_future = None
        else:
            logging.error("no read future on _refresh_rx")

    async def _on_rx(self, sender: BleakGATTCharacteristic, data: bytearray):
        logger.debug(f"on_rx, data: {data} (sender: {sender}, )")

        self.rxbuf += data
        logger.debug(f"rxbuf: {self.rxbuf}")

        if len(self.rxbuf) > self.__class__.MAX_RXBUF_LEN:
            raise BaseException("rxbuf overflow")

        await self._refresh_rx()

from .json_rpc_io import JsonRpcIO
from .locid_jsonrpc_proto_async import LocIdJsonRpcProtocolAsync

class BleJsonRpcClient(JsonRpcIO):
    def __init__(self, bleak_client_or_addr: Union[BleakClient, str]):
        assert bleak_client_or_addr is not None

        nus = BleakNordicNus(bleak_client_or_addr)
        super().__init__(nus)

    async def __aenter__(self):
        print("BleJsonRpcClient AENTER")
        return await super().__aenter__()

class LocIdBleClient(BleJsonRpcClient, LocIdJsonRpcProtocolAsync):

    @property
    def bleak_client(self) -> BleakClient:
        """Accessor for the underlying bleak client"""

        nus: BleakNordicNus = self.io
        return nus.client

    async def connect(self):
        await self.io.connect()

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.bleak_client.address}>"

    def __repr__(self) -> str:
        return self.__str__()

class LocIdBle:

    @classmethod
    async def scan_devices(cls, timeout=5) -> AsyncGenerator[LocIdBleClient, None]:
        """Scans for supported locid bluetooth devices

        (This is an async generator, use with 'async for ...' statement)

        Args:
            timeout: Time to scan for (in seconds)
        """

        queue = asyncio.Queue()

        # duplicate filter
        reported_macs = set()

        def on_det(bleak_dev: BleakClient, advert):
            if not bleak_dev.address in reported_macs:
                dev = LocIdBleClient(bleak_dev)
                queue.put_nowait(dev)
                reported_macs.add(bleak_dev.address)

        bleak_dis_fut = BleakScanner.discover(
            timeout=timeout,
            detection_callback=on_det,
            return_adv=True,
            cb={ "use_bdaddr": True },
            service_uuids=[ LOCID_BLE_SERVICE_UUID ],
            )

        bleak_disc_task = asyncio.create_task(bleak_dis_fut)

        while not bleak_disc_task.done():
            qget = queue.get()
            try:
                dev = await asyncio.wait_for(qget, timeout=1)
                yield dev
            except asyncio.TimeoutError:
                continue

        await asyncio.wait_for(bleak_disc_task, timeout=timeout+1)

    @classmethod
    async def devices(cls, timeout=3) -> List['LocIdBleClient']:
        """Scans for supported locid bluetooth devices and returns them as a list

        Args:
            timeout: Time to scan for (in seconds)
        """

        return [i async for i in LocIdBle.scan_devices(timeout=timeout)]

    @classmethod
    async def scan_print(cls, services=False, timeout=10):

        async for dev in LocIdBle.scan_devices(timeout=timeout):
            print("Found device:", dev)

            try:
                await dev.connect()

                bleak_client = dev.bleak_client

                print("*" * 100)
                print(f"MAC: {bleak_client.address}")

                name_raw = await bleak_client.read_gatt_char(locid_char_uuid_128(LOCID_BLE_UUID_CHAR_NAME))
                name = name_raw.decode()
                print(f"Name (char): {name}")

                fw_raw = await bleak_client.read_gatt_char(locid_char_uuid_128(LOCID_BLE_UUID_CHAR_FIRMWARE_VERSION))
                fw = fw_raw.decode()
                print(f"Firmware: {fw}")

                if services:
                    for service in bleak_client.services:
                        print("\tservice:", service)
                        for char in service.characteristics:
                            print("\t\tchar:", char)

            except Exception as ex:
                print("ex:", ex)
