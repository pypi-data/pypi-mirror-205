import asyncio
import logging
from typing import Dict, Union, List
from numbers import Number
import json
import base64

logger = logging.getLogger('json_rpc_io')
logger.setLevel(logging.INFO)

RFC7464_START = 0x1E
RFC7464_END = 0x0A

class JsonRpcError(BaseException):
    pass

JsonRpcParam = Union[str, int, float, Dict[str, any], List[any]]
JsonRpcResult = Union[str, int, float, Dict[str, any], List[any]]

class JsonRpcIO:
    """ Generic implemention of a json rpc protocol over an (asyncio based) serial transport
    (Framing is currently forced to be in RFC7464 format!).
    """

    rx_task: asyncio.Task
    requests_futures: Dict[any, asyncio.Future]
    req_id: int

    def __init__(self, io):
        self.io = io
        self.req_id = 0
        self.requests_futures = {}

        self.rx_task = asyncio.create_task(self._rx_task_exec())

    async def __aenter__(self):
        logging.debug("jsonrpcio aenter")
        await self.io.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logging.debug("jsonrpcio aexit")
        await self.io.close()
        self.rx_task.cancel()

        try:
            await self.rx_task
        except asyncio.CancelledError:
            logging.debug("rx_task is cancelled now")

    async def _rx_task_exec(self):
        while not self.rx_task.done():
            line = await self.io.readline()
            logging.debug("JSONRPC GOT LINE: {line}")

            if line[0] != RFC7464_START or line[-1] != RFC7464_END:
                raise "malformed rx (missing framing)"

            json_data = line[1:-1]
            j = json.loads(json_data)

            await self._handle_response(j)

    async def _handle_response(self, j: Dict[str, any]):
        if "error" in j:
            id = j["id"]
            future = self.requests_futures[id]
            if future:
                future.set_exception(JsonRpcError(f"err: {j}"))
                del self.requests_futures[id]
        elif "result" in j:
            id = j["id"]
            future = self.requests_futures[id]
            if future:
                future.set_result(j['result'])
                del self.requests_futures[id]
        else:
            raise("todo: jsonrpc notification:", j)

    async def jsonrpc_request(self, method: str, params: JsonRpcParam=None, timeout=10, auto_encode_b64=True) -> JsonRpcResult:
        """ Sends a json rpc request and waits for the result """

        cmd = {
             "method": method,
            "id": self.req_id,
        }

        if params:
            if auto_encode_b64:
                for key, val in params.items():
                    if isinstance(val, bytes) or isinstance(val, bytearray):
                        params[key] = base64.b64encode(val).decode('ascii')

            cmd["params"] = params

        self.req_id += 1

        data = bytes([RFC7464_START]) + json.dumps(cmd).encode() + bytes([RFC7464_END])
        await self.io.write(data)

        fut = asyncio.get_running_loop().create_future()
        self.requests_futures[cmd["id"]] = fut

        try:
            return await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError as ex:
            logging.exception("future wait_for")
            raise JsonRpcError(f"Timeout for request: {cmd} after {timeout}s") from ex

    # compat (remove someday)
    async def request(self, method, params=None, auto_encode_b64=True):
        return await self.jsonrpc_request(method, params, auto_encode_b64)
