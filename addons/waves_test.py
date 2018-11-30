#import logging

import core
#import waves


def handle(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/waves":
		return False
	answer = """<!DOCTYPE html>"""
	answer += """<html><head><meta http-equiv="refresh" content="2"/><title>Waves</title></head><body><h1>Waves</h1>"""
	answer += """</body></html>"""
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


core.addAddon(core.Addon(__name__, handle))
