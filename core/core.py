import os

import conf
from . import db_mongo
from . import fs
from . import protocol


# ==== addons ====

addons = {}

def addAddon(addon):
	addons[addon.name] = addon


# ==== connection ====

connection = {}


# ==== version ====

from collections import namedtuple
# version_info format: (MAJOR, MINOR, MICRO, RELEASE_LEVEL, SERIAL)
# inspired by Python's own sys.version_info, in order to be
# properly comparable using normal operarors, for example:
#  (6,1,0,'beta',0) < (6,1,0,'candidate',1) < (6,1,0,'candidate',2)
#  (6,1,0,'candidate',2) < (6,1,0,'final',0) < (6,1,2,'final',0)
# RELEASE_LEVELS = [ALPHA, BETA, RELEASE_CANDIDATE, FINAL] = ['alpha', 'beta', 'candidate', 'final']
Version = namedtuple('Version', ['major', 'minor', 'micro', 'releaselevel', 'serial'])
version = Version(0, 1, 0, 'alpha', 0)


# ==== init config ====

config = {}
config['MAX_FILE_SIZE'] = conf.MAX_FILE_SIZE
config['SERVER_NAME'] = conf.SERVER_NAME

if os.name == "posix":
	uname = os.uname()
	config['OS_NAME'] = uname.sysname + " " + uname.release + " " + uname.version
else:
	config['OS_NAME'] = os.name


# ==== functions ====

def getHttpData(strdata):
	""" Return named list HTTP POST params
	strdata - utf-8 string
	"""
	res = {}
	pp = strdata.split("\r\n\r\n")
	if len(pp) < 2:
		return res
	params = pp[1].split("&")
	for p in params:
		v = p.split('=')
		if len(v) > 1:
			res[v[0]] = v[1]
	return res


def getHttpHeader(strdata):
	""" Return array of string HTTP HEAD params
	strdata - utf-8 string
	"""
	pp = strdata.split("\r\n\r\n")
	if len(pp) < 1:
		return []
	params = pp[0]
	return params.split("\r\n")


def handle(conn, method, addr, data):
	if addr.startswith('/core/') and (method != "GET"):
		sendAnswer(conn, "400 Bad Request")
		return True
	if addr == '/core/addons':
		answer = '<!DOCTYPE html><html><body>'
		answer += '<h1>Addons</h1>'
		for addonName in addons:
			answer += '<p>'+addonName+'</p>'
		answer += '</body></html>'
		sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
		return True
	if addr == '/core/info':
		answer = '<!DOCTYPE html><html><body>'
		answer += '<h1>Info</h1>'
		answer += '<p>core.config</p>'
		for confName in config:
			answer += '<p>'+confName+'='+str(config[confName])+'</p>'
		answer += '</body></html>'
		sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
		return True
	return False


def handleMessage(msg):
	if msg[v] != 1:
		return False
	return handleMessage1(msg['mt'], msg['of'], msg['to'], msg['data'])


def handleMessage1(mt, of, to, data):
	'''
	mt - message type. See protocol.MessageType
	of - from
	'''
	if to.startswith("a:"):
		addonName = to[2:]
		msg = {}
		msg['v'] = 1
		msg['mt'] = mt
		msg['of'] = of
		msg['to'] = to
		msg['data'] = data
		addons[addonName].handleMessage(msg)
	return True


def handleRecv(conn, addr, data):
	connection['conn'] = conn
	connection['addr'] = addr
	connection['data'] = data
	udata = data.decode("utf-8")
	# take only the first line
	udata2 = udata.split("\r\n", 1)[0]
	# we divide our line by spaces
	method, address, protocol = udata2.split(" ", 2)
	connection['method'] = method
	connection['address'] = address
	connection['protocol'] = protocol
	print(addr, protocol, method, address)
	if not protocol.startswith("HTTP/1"):
		return    # do not process
	if (len(address) < 1) or (address[0] != '/'):
		address = "/" + address
	if handle(conn, method, address, udata):
		return
	if address == '/':
		address = '/index.html'
	for addonName in addons:
		if addons[addonName].handleHttp(conn, method, address, udata):
			break


def sendAnswer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=b"", maxage=0):
	conn.send(b"HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
	s = "Server: " + config['SERVER_NAME'] +" (" + config['OS_NAME'] + ")\r\n"
	conn.send(s.encode("utf-8"))
	if maxage > 0:
		s = "Cache-Control: max-age=" + str(maxage) + ", must-revalidate\r\n"
		conn.send(s.encode("utf-8"))
	else:
		conn.send(b"Cache-Control: no-cache, no-store, must-revalidate\r\n")
	conn.send(b"Connection: close\r\n")
	conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
	s = "Content-Length: " + str(len(data)) + "\r\n"
	conn.send(s.encode("utf-8"))
	conn.send(b"Content-Language: en, ru\r\n")
	conn.send(b"\r\n") # after the empty string in HTTP data begins
	conn.send(data)


# fn - file name
def sendAnswerFile(conn, fn, typ="image/png"):
	try:
		if not os.path.exists(fn):
			sendAnswer(conn, "404 Not Found")
			return 404
		fSize = os.path.getsize(fn)
		if fSize > config['MAX_FILE_SIZE']:
			print("FileSize ",fSize," > MAX_FILE_SIZE: ",fn)
			s = "Requested file is too big "+str(fSize) +">"+str(config['MAX_FILE_SIZE'])
			sendAnswer(conn, data=s.encode('utf-8'))
			return 1
		r = 0
		file = open(fn, 'rb')
		try:
			sendAnswer(conn, "200 OK", typ, file.read(config['MAX_FILE_SIZE']), 3600)
		except Exception as e:
			r = 500
			sendAnswer(conn, "500 Internal Server Error")
			print(e)
		finally:
			file.close()
	except Exception as e:
		r = 500
		sendAnswer(conn, "500 Internal Server Error")
		print(e)
	return r
