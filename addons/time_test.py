import time

import core


def handleHttp(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/time":
		return False
	answer = """<!DOCTYPE html>"""
	answer += """<html><head><meta http-equiv="refresh" content="2"/><title>Time</title></head><body><h1>"""
	answer += time.strftime("%H:%M:%S %d.%m.%Y")
	answer += """</h1></body></html>"""
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
