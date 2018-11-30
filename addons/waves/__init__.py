import core
from . import waves


def handleHttp(conn, method, addr, data):
	if (addr == "/api/waves/height") and (method == "GET"):
		h = waves.height();
		answer = '{"height":"'+str(h)+'"}'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	return False


def handleMessage(data):
	print(__name__, ' ', data)


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
