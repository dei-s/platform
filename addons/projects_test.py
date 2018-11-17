import core


def handle(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/projects":
		return False
	answer = '<!DOCTYPE html>'
	answer += '<html><head><meta charset="utf-8"><title>Projects</title></head><body><h1>Projects</h1>'
	answer += '<div>Test</div>'
	answer += '<form action="/api/project" method="POST"><input type="submit" value="Submit POST /api/project"> OK</form>'
	answer += '<form action="/api/project/0" method="POST"><input type="submit" value="Submit POST /api/project/0"> Error 400</form>'
	answer += '<form action="/api/project" method="POST"><input name="title" value="Test1"><input type="submit" value="Submit POST"> OK</form>'
	answer += '<form action="/api/project" method="POST"><input name="title" value="Test1"><input name="description" value="Description"><input name="status" value="100"><input name="img" value="/favicon.ico"><input type="submit" value="Submit POST"></form>'
	answer += '<form action="/api/getProjects" method="POST"><input name="testParam1" value="Test1"><input name="testParam2" value="Test2"><input type="submit" value="GetProjects"></form>'
	answer += '</body></html>'
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handle))
