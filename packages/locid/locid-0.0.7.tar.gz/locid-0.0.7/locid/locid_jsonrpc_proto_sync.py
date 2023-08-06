
class LocIdJsonRpcProtocol:
    """
    Kept for compatibility. Use LocIdJsonRpcProtocolAsync!
    """

    PROXIMITY_NONE = 0
    """ Numeric proximity level for 'none/'outside' range """
    PROXIMITY_NEAR = 1
    """ Numeric proximity level for 'near' range """
    PROXIMITY_FAR = 2
    """ Numeric proximity level for 'far' range """

    def jsonrpc_call(self, cmd, params=None):
        raise BaseException("This is class in meant to be a mixin, don't use directly")

    def ping(self, echo=None):
        """
        Ping locid module
        """
        return self.jsonrpc_call('locid.ping', { "echo": echo })

    def restart(self):
        """
        Restarts firmware (3 seconds after call).
        """
        return self.jsonrpc_call('locid.restart')

    def getVersion(self):
        """
        Gets firmware version information
        """
        return self.jsonrpc_call('locid.getVersion')

    def getStatus(self):
        """
        Gets status (connected users, activation state, ...)
        """
        return self.jsonrpc_call('locid.getStatus')

    def getState(self):
        """
        Gets state (connected users, activation state, ...)
        """
        return self.jsonrpc_call('locid.getState')

    def getBeaconId(self):
        """
        Gets the unique beacon id of this module
        """
        return self.jsonrpc_call('locid.getBeaconId')

    def getMetaInfo(self):
        """
        Reads meta information descriptor (raw)
        """
        return self.jsonrpc_call('locid.getMetaInfo')

    def setMetaInfo(self, metaInfo=None):
        """
        Writes meta information descriptor (raw)
        """
        return self.jsonrpc_call('locid.setMetaInfo', { "metaInfo": metaInfo })

    def getNear(self):
        """
        Gets near range threshold
        """
        return self.jsonrpc_call('locid.getNear')

    def setNear(self, near=None):
        """
        Sets near range threshold
        """
        return self.jsonrpc_call('locid.setNear', { "near": near })

    def getFar(self):
        """
        Gets far range threshold
        """
        return self.jsonrpc_call('locid.getFar')

    def setFar(self, far=None):
        """
        Sets far range threshold
        """
        return self.jsonrpc_call('locid.setFar', { "far": far })

    def getBeaconRSSI(self):
        """
        Gets beacon calibration value
        """
        return self.jsonrpc_call('locid.getBeaconRSSI')

    def setBeaconRSSI(self, rssi:int=None):
        """
        Sets beacon calibration value (RSSI in 1m distance)
        """
        return self.jsonrpc_call('locid.setBeaconRSSI', { "rssi": rssi })

    def getTxPower(self):
        """
        Gets bluetooth transmission power
        """
        return self.jsonrpc_call('locid.getTxPower')

    def setTxPower(self, txpower:int=None):
        """
        Sets bluetooth transmission power
        """
        allowed = [-40, -20, -16, -12, -8, -4, 0, 3, 4, 8]
        if not txpower in allowed:
            raise BaseException(f"Invalid arg, allowed: {allowed}")

        return self.jsonrpc_call('locid.setTxPower', { "txpower": txpower })

    def enable_advanced_stats(self, enable):
        """
        Enables advanced debugging statistics (for locid.getStatus)
        """

        return self.jsonrpc_call("locid.setEnableAdvancedStatistics", {"enable": enable})