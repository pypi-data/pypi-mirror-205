#!/usr/bin/env python3

import json
import time
import os
import logging
from threading import Thread, Condition, Event

import serial
import serial.tools.list_ports

from .locid_jsonrpc_proto_sync import LocIdJsonRpcProtocol

logger = logging.getLogger('locid_usb')
logger.setLevel(logging.DEBUG)

LOCID_USB_VID = 21018
LOCID_USB_PID = 1


class LocIdError(BaseException):
    pass


class JsonRPCError(LocIdError):
    pass


class TransportError(LocIdError):
    pass


def find_serial_port() -> str:
    for port in serial.tools.list_ports.comports():
        logging.debug(f"port: {port}, path: {port.device}, vid: {port.vid}, pid: {port.pid}")

        if port.vid == LOCID_USB_VID and port.pid == LOCID_USB_PID:
            return port.device

    return None


class LocIdSerialTransportThread(Thread):

    def __init__(self, device_port: str = None):
        """ Initializes and connects LocId serial transport instance.

        :param device_port: Serial port of locid module. Use e.g. "COMX" on windows, "/dev/ttyUSB*" on unix. If omitted, the device is tried to be determined automatically.
        """

        Thread.__init__(self)
        self.daemon = True
        self.device_port = device_port
        self.serial = None

        self._jsonrpc_id = 0
        self._error_callback = None
        self._status_callback = None
        self._notification_callback = None
        self._user_action_callback = None
        self._usb_forward_callback = None
        self._user_connected_callback = None
        self._user_disconnected_callback = None

        self.jsonrpc_conds = dict()
        self.jsonrpc_responses = dict()

        self._users_by_id = {}
        self._stop_rx_thread_evt = Event()

    def connect_serial(self):
        if not self.device_port:
            self.device_port = os.environ.get('DEV')
        if not self.device_port:
            self.device_port = find_serial_port()
        if not self.device_port:
            raise TransportError("Couldn't auto-detect serial interface (use DEV environment variable, e.g. DEV=COM1 or DEV=/dev/ttyUSB0)")

        logging.info("using device port: %s", self.device_port)
        self.serial = serial.Serial(self.device_port)
        self.start()

    def connect(self):
        self.connect_serial()

    def close(self):
        logging.debug("close")
        self._stop_rx_thread_evt.set()
        self.serial.close()
        self.join()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def jsonrpc_call(self, method, params=None, ignore_response=False):
        """ Sends a locid protocol request.
        (see https://locid.org/dev/jsonrpc-doc/)

        :param method: method name (e.g. locid.ping)
        :param params: parameter dictionary (optional)
        :param ignore_response: If True, this call won't block and ignore results
        :returns: result object
        """

        if self.serial is None:
            logging.warning("please call connect() explicitly before")
            self.connect_serial()

        # see https://www.jsonrpc.org/specification
        jsonrpc_id = self._jsonrpc_id
        self._jsonrpc_id += 1

        request_j = {
            "id": jsonrpc_id,
            "method": method,
        }
        if params:
            request_j['params'] = params

        lock = Condition()
        self.jsonrpc_conds[jsonrpc_id] = lock

        bytes = (json.dumps(request_j) + "\n").encode()
        logging.debug("sending bytes: %s, len: %d", bytes, len(bytes))
        self.serial.write(bytes)
        self.serial.flush()

        if ignore_response:
            return None

        with lock:
            lock.wait(10)

        if jsonrpc_id not in self.jsonrpc_responses:
            raise JsonRPCError(f"no response for jsonrpc request {jsonrpc_id}")

        res_j = self.jsonrpc_responses[jsonrpc_id]

        del self.jsonrpc_responses[jsonrpc_id]

        if "error" in res_j:
            raise JsonRPCError(f"jsonrpc error: {res_j} (request: {request_j})")
        else:
            return res_j.get("result")

    def reset(self):
        """ Restarts firmware """
        self._stop_rx_thread_evt.set()
        res = self.jsonrpc_call("locid.restart", ignore_response=True)
        return res

    def dfu(self):
        """ Enters DFU mode """

        logging.info("stopping tx thread...")
        self._stop_rx_thread_evt.set()
        res = self.jsonrpc_call("locid.enterUsbDfu", ignore_response=True)
        time.sleep(3)
        logging.info("closing serial")
        self.serial.close()
        return res

    def on_status(self, callback):
        self._status_callback = callback

    def on_error(self, callback):
        self._error_callback = callback

    def on_client_request(self, callback):
        self._usb_forward_callback = callback

    def on_notification(self, callback):
        """" Sets a (generic) notification handler """
        self._notification_callback = callback

    def on_user_action(self, callback):
        """" Sets a user action handler (e.g. handsender button press events) """
        self._user_action_callback = callback

    def on_user_min_prox_changed(self, old, prox):
        logging.info("on_user_min_prox_changed", old, prox)

    def on_user_connected(self, user_id):
        logging.info("on_user_connected: %s", user_id)
        if self._user_connected_callback:
            self._user_connected_callback(self, user_id)
        pass

    def on_user_disconnected(self, user_id):
        logging.info("on_user_disconnected: %s", user_id)
        if self._user_disconnected_callback:
            self._user_disconnected_callback(self, user_id)
        pass

    def on_user_proximity_changed(self, user_id):
        pass

    def handle_status_notification(self, status):
        # print("handle_status_notification:", status)

        if "users" in status:
            connected_before = set(filter(lambda u: self._users_by_id[u].get('connected', False), self._users_by_id.keys()))
            # print("connected_before:", connected_before)

            for u in self._users_by_id.values():
                u['connected'] = False

            for u in status["users"]:
                uid = u["id"]
                if uid not in self._users_by_id:
                    self._users_by_id[uid] = u

                self._users_by_id[uid]['connected'] = True

                if uid not in connected_before:
                    self.on_user_connected(uid)

            for uid in connected_before:
                if not self._users_by_id[uid]['connected']:
                    self.on_user_disconnected(uid)

        if self._status_callback:
            self._status_callback(status)

    def run(self):
        while not self._stop_rx_thread_evt.is_set():
            # print("waiting for line...")
            line = None
            try:
                line = self.serial.readline()
            except serial.serialutil.SerialException as e:
                stopped = self._stop_rx_thread_evt.is_set()
                if stopped:
                    break
                else:
                    logger.exception(f"Serial ex, stop: {stopped}")
                    raise TransportError("serial disconnect") from e

            logging.debug("<<< %s", line)

            j = None
            try:
                j = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                logging.error("json dec error: %s", e)
                logging.error("in line: %s", line)
                if self._error_callback:
                    self._error_callback(e)
                continue

            # logging.debug("json: %s", j)

            # jsonrpc responses (and errors)
            if 'id' in j:
                self.jsonrpc_responses[j['id']] = j
                cond = self.jsonrpc_conds[j['id']]
                with cond:
                    cond.notify()
                del self.jsonrpc_conds[j['id']]

            # jsonrpc notifications
            elif 'method' in j:
                method = j['method']
                params = j.get("params")
                if method == 'locid.status':
                    self.handle_status_notification(j['result'])

                elif method == 'locid.usbForward' or method == 'locid.hostForward':
                    logging.debug("locid.usbForward: %s", j)

                    data = j.get("params", {}).get("data")
                    if data is None:
                        logging.error("missing data arg")
                    else:
                        if self._usb_forward_callback:
                            self._usb_forward_callback(data)

                if self._notification_callback:
                    self._notification_callback(j)

                if method == 'locid.user.action' and self._user_action_callback is not None:
                    action_id = params['action_id']
                    self._user_action_callback(action_id, params)

                # elif method == 'locid.user.prox_changed':
                #     print("TODO")

        logging.debug("thread exit")


class LocIdUSBDongle(LocIdSerialTransportThread, LocIdJsonRpcProtocol):

    @classmethod
    def all(cls):
        res = []
        for port in serial.tools.list_ports.comports():
            logging.debug(f"port: {port}, path: {port.device}, vid: {port.vid}, pid: {port.pid}")

            if port.vid == LOCID_USB_VID and port.pid == LOCID_USB_PID:
                res.append(LocIdUSBDongle(port.device))

        return res


# compat
class LocId(LocIdUSBDongle):
    """ Deprecated: Use LocIdUSBDongle """
    pass
