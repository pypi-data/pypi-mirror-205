import asyncio

class LocIdJsonRpcProtocolAsync:
    """
    Mix-in for jsonrpc abstractions
    """

    PROXIMITY_NONE = 0
    """ Numeric proximity level for 'none/'outside' range """
    PROXIMITY_NEAR = 1
    """ Numeric proximity level for 'near' range """
    PROXIMITY_FAR = 2
    """ Numeric proximity level for 'far' range """

    async def jsonrpc_request(self, cmd, params=None):
        raise BaseException("This is class in meant to be a mixin, don't use this directly. When subclassing, provide a jsonrpc_call method in super")

    async def login(self, pin):
        """
        Login with pin (required for wireless transports)
        """

        auth_state = await self.jsonrpc_request('blx.getAuthState')
        print("auth_state:", auth_state)

        if auth_state["needsPinSetup"] == True:
            return await self.jsonrpc_request('blx.login', { "pin": "" })
        else:
            return await self.jsonrpc_request('blx.login', { "pin": pin })

    async def ping(self, echo=None):
        """
        Ping locid module
        """
        return await self.jsonrpc_request('locid.ping', { "echo": echo })

    async def restart(self, ):
        """
        Restarts firmware (3 seconds after call).
        """
        return await self.jsonrpc_request('locid.restart')

    async def getVersion(self, ):
        """
        Gets firmware version information
        """
        return await self.jsonrpc_request('locid.getVersion')

    async def getStatus(self, ):
        """
        Gets status (connected users, activation state, ...)
        """
        return await self.jsonrpc_request('locid.getStatus')

    async def getBeaconId(self, ):
        """
        Gets the unique beacon id of this module
        """
        return await self.jsonrpc_request('locid.getBeaconId')

    async def getMetaInfo(self, ):
        """
        Reads meta information descriptor (raw)
        """
        return await self.jsonrpc_request('locid.getMetaInfo')

    async def setMetaInfo(self, metaInfo=None):
        """
        Writes meta information descriptor (raw)
        """
        return await self.jsonrpc_request('locid.setMetaInfo', { "metaInfo": metaInfo })

    async def getNear(self, ):
        """
        Gets near range threshold
        """
        return await self.jsonrpc_request('locid.getNear')

    async def setNear(self, near=None):
        """
        Sets near range threshold
        """
        return await self.jsonrpc_request('locid.setNear', { "near": near })

    async def getFar(self, ):
        """
        Gets far range threshold
        """
        return await self.jsonrpc_request('locid.getFar')

    async def setFar(self, far=None):
        """
        Sets far range threshold
        """
        return await self.jsonrpc_request('locid.setFar', { "far": far })

    async def getBeaconRSSI(self, ):
        """
        Gets beacon calibration value
        """
        return await self.jsonrpc_request('locid.getBeaconRSSI')

    async def setBeaconRSSI(self, rssi:int=None):
        """
        Sets beacon calibration value (RSSI in 1m distance)
        """
        return await self.jsonrpc_request('locid.setBeaconRSSI', { "rssi": rssi })

    async def getTxPower(self, ):
        """
        Gets bluetooth transmission power
        """
        return await self.jsonrpc_request('locid.getTxPower')

    async def setTxPower(self, txpower:int=None):
        """
        Sets bluetooth transmission power
        """
        allowed = [-40, -20, -16, -12, -8, -4, 0, 3, 4, 8]
        if not txpower in allowed:
            raise BaseException(f"Invalid arg, allowed: {allowed}")

        return await self.jsonrpc_request('locid.setTxPower', { "txpower": txpower })

    async def enable_advanced_stats(self, enable):
        """
        Enables advanced debugging statistics (for locid.getStatus)
        """

        return await self.jsonrpc_request("locid.setEnableAdvancedStatistics", {"enable": enable})