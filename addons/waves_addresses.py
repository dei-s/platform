import core
from . import waves


def handleHttp(conn, method, addr, data):
	if (method == "GET") and (addr.startswith("/api/addresses/balance/")):
		waves.apiAddressesBalance(conn, addr[23:])
		return True
	return False


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
