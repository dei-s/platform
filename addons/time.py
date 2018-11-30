import time

import core


def handleHttp(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/api/getTime":
		return False
	answer = '{"time": "'+time.strftime("%H:%M:%S %d.%m.%Y")+'"}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
