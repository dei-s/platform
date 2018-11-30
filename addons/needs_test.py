import core


def handleHttp(conn, method, addr, data):
	if method != "GET":
		return False
	if addr != "/test/needs":
		return False
	answer = '<!DOCTYPE html>'
	answer += '<html><head><meta charset="utf-8"><title>Needs Test</title></head><body><h1>Needs</h1>'
	answer += '<div>Test</div>'
	answer += '<p><a href="/api/needsCount">GET /api/needsCount</a></p>'
	answer += '<p><a href="/api/getNeedsCount">GET /api/getNeedsCount</a></p>'
	answer += '<p><a href="/api/needs">GET /api/needs</a></p>'
	answer += '<p><a href="/api/need/5bf072b91a89170676a4b5bc">GET /api/need/5bf072b91a89170676a4b5bc</a></p>'
	answer += '<form action="/api/getNeed" method="GET"><input name="id" value="1"><input type="submit" value="GET /api/getNeed"></form>'
	answer += '<form action="/api/need" method="POST"><input type="submit" value="POST /api/need"></form>'
	answer += '<form action="/api/need" method="POST"><input name="title" value="Test1"><input type="submit" value="POST /api/need"></form>'
	answer += '<form action="/api/need" method="POST"><input name="title" value="Test1"><input name="description" value="Description"><input type="submit" value="POST /api/need"></form>'
	answer += '<form action="/api/needs" method="POST"><input type="submit" value="POST /api/needs"></form>'
	answer += '</body></html>'
	core.sendAnswer(conn, typ="text/html; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleMessage(msg):
	return False


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
