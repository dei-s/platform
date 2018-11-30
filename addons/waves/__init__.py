import core
from . import waves


def handle(conn, method, addr, data):
	if (addr == "/api/waves/height") and (method == "GET"):
		h = waves.height();
		print(h)
		answer = '{"height":"'+str(h)+'"}'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	return False


print(__name__)
core.addAddon(core.Addon(__name__, handle))
