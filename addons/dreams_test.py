import core


def handleHttp(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/dreams":
		return False
	answer = '<!DOCTYPE html>'
	answer += '<html><head><meta charset="utf-8"><title>Dreams Test</title></head><body><h1>Dreams</h1>'
	answer += '<div>Test</div>'
	answer += '<p><a href="/api/dreamsCount">GET /api/dreamsCount</a></p>'
	answer += '<p><a href="/api/getDreamsCount">GET /api/getDreamsCount</a></p>'
	answer += '<p><a href="/api/dreams">GET /api/dreams</a></p>'
	answer += '<p><a href="/api/dream/5bf066e31a8917768bac3819">GET /api/dream/5bf066e31a8917768bac3819</a></p>'
	answer += '<form action="/api/getDream" method="GET"><input name="id" value="1"><input type="submit" value="GET /api/getDream"></form>'
	answer += '<form action="/api/dream" method="POST"><input type="submit" value="POST /api/dream"></form>'
	answer += '<form action="/api/dream" method="POST"><input name="title" value="Test1"><input type="submit" value="POST /api/dream"></form>'
	answer += '<form action="/api/dream" method="POST"><input name="title" value="Test1"><input name="description" value="Description"><input type="submit" value="POST /api/dream"></form>'
	answer += '<form action="/api/dreams" method="POST"><input type="submit" value="POST /api/dreams"></form>'
	answer += '</body></html>'
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
