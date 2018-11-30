import os
import sys

import conf
import core

from . import mime


# ==== Config ====

if 'STATIC_DIR' in dir(conf):
	if len(conf.STATIC_DIR) > 0 and conf.STATIC_DIR.startswith("/"):
		STATIC_DIR = conf.STATIC_DIR
	else:
		STATIC_DIR = os.path.dirname(__file__)+'/../../'+conf.STATIC_DIR
else:
	STATIC_DIR = os.path.dirname(__file__)+'/../../http_static'

if len(sys.argv) > 2:
	if sys.argv[1] == "--staticdir":
		STATIC_DIR = sys.argv[2]

STATIC_DIR = os.path.abspath(STATIC_DIR)
core.config['STATIC_DIR'] = STATIC_DIR


# ==== Functions ====

def handleHttp(conn, method, addr, data):
	if method != "GET":
		core.sendAnswer(conn, typ="400 Bad Request: Static files must GET")
		return False
	for ext in mime.STATIC_MIME:
		if addr.endswith("."+ext):
			return core.sendAnswerFile(conn, STATIC_DIR + addr, mime.STATIC_MIME[ext])
	if core.fs.isFileDoctypeHtml(STATIC_DIR + addr):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/html")
	else:
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/plain");

def handleMessage(msg):
	return False
