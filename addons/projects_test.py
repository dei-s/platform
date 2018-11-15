import core


def handle(conn, addr, method, data):
	if method != "GET":
		return False
	if addr != "/test/projects":
		return False
	answer = '<!DOCTYPE html>'
	answer += '<html><head><meta charset="utf-8"><title>Projects</title></head><body><h1>Projects</h1>'
	answer += '<div>Test</div>'
	answer += '<form action="/api/project/0" method="POST"><input type="submit" value="Submit POST"></form>'
	answer += '<form action="/api/project/1" method="POST"><input name="testParam1" value="Test1"><input type="submit" value="Submit POST"></form>'
	answer += '<form action="/api/project/2" method="POST"><input name="testParam1" value="Test1"><input name="testParam2" value="Test2"><input type="submit" value="Submit POST"></form>'
	answer += '<form action="/api/getProjects" method="POST"><input name="testParam1" value="Test1"><input name="testParam2" value="Test2"><input type="submit" value="GetProjects"></form>'
	answer += '</body></html>'
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handle))
