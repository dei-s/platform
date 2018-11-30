import core


def handleHttp(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/waves":
		return False
	answer = """<!DOCTYPE html>"""
	answer += """<html><head><meta http-equiv="refresh" content="30"/><title>Waves</title></head><body><h1>Waves</h1>"""
	answer += """</body></html>"""
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
