#!/usr/bin/python3

import os
import socket
import sys

import conf
import core
from addons import dreams
from addons import dreams_test
from addons import needs
from addons import needs_test
from addons import projects
from addons import projects_test
from addons import time
from addons import time_test
from addons import waves
from addons import waves_addresses
from addons import waves_test
# Static addon must be the last. If previous addons have not processed the request, then search in static files.
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
	core.handleRecv(conn, addr, data)


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
