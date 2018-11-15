import os

import conf


def isFileDoctypeHtml(fn):
	""" Return true if file started from "<!DOCTYPE html" or "<!DOCTYPE HTML"
	fn - file name
	"""
	try:
		if not os.path.exists(fn):
			return False
		line = ""
		file = open(fn, 'r', encoding="utf-8")
		try:
			line = file.readline()
		finally:
			file.close()
		if line.startswith("<!DOCTYPE html") or line.startswith("<!DOCTYPE HTML"):
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False


def log(s):
	print('[core.fs]: '+s)
