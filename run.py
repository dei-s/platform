#!/usr/bin/python3

import os
import socket
import sys

import conf
import core
from addons import projects
from addons import projects_test
from addons import time
from addons import time_test
from addons import static


# ==== functions ====

def Parse(conn, addr):
	data = b""

	while not b"\r\n" in data: # waiting for the first line
		tmp = conn.recv(1024)
		if not tmp:   # socket closed, empty object
			break
		else:
			data += tmp

	if not data:      # data did not come
		return        # do not process

	udata = data.decode("utf-8")
	# take only the first line
	udata2 = udata.split("\r\n", 1)[0]
	# we divide our line by spaces
	method, address, protocol = udata2.split(" ", 2)
	print(addr, "method="+method+" address="+address+" protocol="+protocol)

	if not protocol.startswith("HTTP/1"):
		return    # do not process

	if (len(address) < 1) or (address[0] != '/'):
		address = "/" + address
	if address == '/':
		address = '/index.html'
	for addonName in core.addons:
		if core.addons[addonName].handle(conn, address, method, udata):
			break


# ==== main ====

sock = socket.socket()
sock.bind((conf.HOST, conf.PORT))
sock.listen(5)
try:
	while 1:
		conn, addr = sock.accept()
		try:
			Parse(conn, addr)
		except Exception as e:
			core.sendAnswer(conn, "500 Internal Server Error")
			print(e)
		finally:
			conn.close()
finally:
	sock.close()
