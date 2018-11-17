import os
import sys

import conf
import core


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

def handle(conn, method, addr, data):
	if method != "GET":
		core.sendAnswer(conn, typ="400 Bad Request")
		return False
	if addr.endswith(".ico"):
		return core.sendAnswerFile(conn, STATIC_DIR + addr, "image/png")
	elif addr.endswith(".gif"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/gif")
	elif addr.endswith(".jpeg") or addr.endswith(".jpg"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/jpeg")
	elif addr.endswith(".png"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/png")
	elif addr.endswith(".svg"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/svg+xml")
	elif addr.endswith(".tiff"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/tiff")
	elif addr.endswith(".webp"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "image/webp")
	elif addr.endswith(".pdf"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "application/pdf")
	elif addr.endswith(".js"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "application/javascript")
	elif addr.endswith(".json"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "application/json")
	elif addr.endswith(".zip"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "application/zip")
	elif addr.endswith(".gzip"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "application/gzip")
	elif addr.endswith(".mp4"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "audio/mp4")
	elif addr.endswith(".aac"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "audio/aac")
	elif addr.endswith(".mp3"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "audio/mpeg")
	elif addr.endswith(".ogg"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "audio/ogg")
	elif addr.endswith(".css"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/css")
	elif addr.endswith(".csv"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/csv")
	elif addr.endswith(".css"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/css")
	elif addr.endswith(".html") or addr.endswith(".htm"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/html")
	elif addr.endswith(".txt"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/plain")
	elif addr.endswith(".php"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/php")
	elif addr.endswith(".xml"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/xml")
	elif addr.endswith(".md"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/markdown")
	elif addr.endswith(".mpeg") or addr.endswith(".mpg") or addr.endswith(".avi"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "video/mpeg")
	elif addr.endswith(".mp4") or addr.endswith(".mp5"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "video/mp4")
	elif addr.endswith(".webm"):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "video/webm")
	elif core.fs.isFileDoctypeHtml(STATIC_DIR + addr):
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/html")
	else:
		core.sendAnswerFile(conn, STATIC_DIR + addr, "text/plain");


def log(s):
	print('['+__name__+']: '+s)
