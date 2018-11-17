import core


def handle(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/projects":
		return False
	answer = '<!DOCTYPE html>'
	answer += '<html><head><meta charset="utf-8"><title>Projects</title></head><body><h1>Projects</h1>'
	answer += '<div>Test</div>'
	answer += '<p><a href="/api/project/5bf03f611a89174156a2e6d5">/api/project/5bf03f611a89174156a2e6d5</a></p>'
	answer += '<p><a href="/api/getProject?id=5beb05c71a89173c9ee18bc6">/api/project?id=5beb05c71a89173c9ee18bc6</a></p>'
	answer += '<p><a href="/api/projectsCount">/api/projectsCount</a></p>'
	answer += '<p><a href="/api/getProjectsCount">/api/getProjectsCount</a></p>'
	answer += '<p><a href="/api/getProjects">/api/getProjects</a></p>'
	answer += '<form action="/api/project" method="POST"><input type="submit" value="POST /api/project"></form>'
	answer += '<form action="/api/project" method="POST"><input name="title" value="Test1"><input type="submit" value="POST"></form>'
	answer += '<form action="/api/project" method="POST"><input name="title" value="Test1"><input name="description" value="Description"><input name="status" value="100"><input name="img" value="/favicon.ico"><input type="submit" value="POST"></form>'
	answer += '<form action="/api/getProjects" method="POST"><input name="testParam1" value="Test1"><input name="testParam2" value="Test2"><input type="submit" value="POST GetProjects"></form>'
	answer += '</body></html>'
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handle))
