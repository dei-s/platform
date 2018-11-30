import datetime

import core


def _apiGetNeed(conn, needId):
	needId = bytes(needId, "utf-8").decode("unicode_escape").strip().replace('"','')
	if needId == "":
		core.sendAnswer(conn, "400 Bad Request: needId is empty")
		return True
	try:
		item = core.db.needs.find_one({"_id": core.ObjectId(needId)})
	except Exception as e:
		log("500 Internal Server Error: "+str(e))
		core.sendAnswer(conn, "500 Internal Server Error: "+str(e))
		return True
	if item == None:
		answer = '{}'
	else:
		answer = str(item)
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	return True


def _getPostData(data):
	""" Return list of string POST params
	data - utf-8 string
	"""
	params = data.split("\r\n\r\n")[1]
	return params.split("&")


def _getNeedsCountJson(conn):
	count = core.db.needs.find().count()
	answer = '{"needsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def _insertNeed(title, description):
	post1 = {"title": title, "description": description, "createDate": datetime.datetime.utcnow()}
	return core.db.needs.insert(post1)


def _needItemToStr(item):
	s = '{"id":"'+str(item["_id"])+'",'
	if 'title' in item:
		s += '"title":"'+str(item["title"]).replace('"','')+'",'
	if 'description' in item:
		s += '"description":'+str(item["description"]).replace('"','')+'",'
	if 'createDate' in item:
		dts = item['createDate'].isoformat().split('.')[0]
		s += '"createDate":"'+str(dts)+'",'
		tt = item['createDate'].timetuple()
		if len(tt) >= 6:
			s += '"createYear":"'+str(tt[0])+'",'
			s += '"createMonth":"'+str(tt[1])+'",'
			s += '"createDay":"'+str(tt[2])+'",'
			s += '"createHour":"'+str(tt[3])+'",'
			s += '"createMinute":"'+str(tt[4])+'",'
			s += '"createSecond":"'+str(tt[5])+'",'
	s = s[:-1] # remove end ,
	return s + '},'


def handleHttp(conn, method, addr, data):
	""" API Request handler (/api)
	method - GET/POST/PUT/DELETE
	data - utf-8 string
	"""
	if (addr == "/api/need") or addr.startswith("/api/need/"):
		return handleApiNeed(conn, method, addr, data)
	if addr == "/api/needs":
		return handleApiNeeds(conn, method, addr, data)
	if addr == "/api/needsCount":
		return handleApiNeedsCount(conn, method, addr, data)
	if (addr == "/api/getNeed") or addr.startswith("/api/getNeed?"):
		return handleApiGetNeed(conn, method, addr, data)
	if addr == "/api/getNeeds" or addr.startswith("/api/getNeeds?"):
		return handleApiGetNeeds(conn, method, addr, data)
	if addr == "/api/getNeedsCount":
		return handleApiGetNeedsCount(conn, method, addr, data)
	if addr.startswith("/api/getNeedCard/"):
		return handleApiGetNeedCard(conn, method, addr, data)
	if addr == "/api/getNeed":
		core.sendAnswer(conn, "400 Bad Request in Needs addon")
		return True
	return False


def handleApiGetNeed(conn, method, addr, data):
	if method != "GET":
		core.sendAnswer(conn, "400 Bad Request: /api/getNeed must is GET")
		return True
	_apiGetNeed(conn, addr[16:])
	return True


def handleApiGetNeedCard(conn, method, addr, data):
	needId = addr[19:]
	needId = bytes(needId, "utf-8").decode("unicode_escape").strip().replace('"','')
	answer = '<div class="divBlock divNeedBlockOk"><h3>'+needId+'</h3><p>Need1</p></div>'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleApiGetNeeds(conn, method, addr, data):
	if (method == "GET") or (method == "POST"):
		items = core.db.needs.find().limit(1000)
		answer = "["
		for item in items:
			answer += _needItemToStr(item)
		if answer.endswith(','):
			answer = answer[:-1]
		answer += ']'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/getNeeds must GET or POST")
	return True


def handleApiGetNeedsCount(conn, method, addr, data):
	if method == "GET":
		_getNeedsCountJson(conn)
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/getNeedsCount must GET")
	return True


def handleApiNeed(conn, method, addr, data):
	if method == "GET":
		# Возвращает информацию о проекте в формате JSON
		_apiGetNeed(conn, addr[10:])
	elif method == "POST":
		# Добавляет новый проект. Если указан id то возвращает ошибку 400.
		params = _getPostData(data)
		nId = addr[13:]
		if nId != "":
			core.sendAnswer(conn, "400 Bad Request: POST /api/need/xxxx ID is not empty")
			return True
		pTitle = ""
		pDescription = ""
		pInvestments = ""
		pGoal = ""
		pStatus = ""
		pImg = ""
		par = {}
		for p in params:
			if p == "":
				continue
			p = p.split("=")
			if len(p) < 2:
				continue
			if p[0] == 'id':
				core.sendAnswer(conn, "400 Bad Request: POST /api/need/ ID is not empty")
				return True
			if p[0] == 'title':
				pTitle = p[1]
			if p[0] == 'description':
				pDescription = p[1]
			par[p[0]] = p[1]
		nId = _insertNeed(pTitle, pDescription)
		item = core.db.needs.find_one({"_id": core.ObjectId(nId)})
		if item == None:
			answer = '{}'
		else:
			answer = str(item)
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	elif method == "PUT":
		# Если указан id то обновляет информацию о проекте в формате JSON иначе возвращает ошибку 400
		params = _getPostData(data)
		nId = 0
		pTitle = ""
		pDescription = ""
		pInvestments = ""
		pGoal = ""
		pStatus = ""
		pImg = ""
		par = {}
		for p in params:
			if p == "":
				continue
			p = p.split("=")
			if len(p) < 2:
				continue
			if p[0] == 'id':
				pId = core.ObjectId(p[1])
			if p[0] == 'title':
				pTitle = p[1] 
			if p[0] == 'description':
				pDescription = p[1] 
			if p[0] == 'investments':
				pInvestments = p[1] 
			if p[0] == 'goal':
				pGoal = p[1] 
			if p[0] == 'status':
				pStatus = p[1] 
			if p[0] == 'img':
				pImg = p[1] 
			par[p[0]] = p[1]
		log(par)
		if nId == 0:
			core.sendAnswer(conn, "400 Bad Request: PUT /api/need/ ID is empty")
			return True
		#item = core.db.needs.find_one({"_id": core.ObjectId(needId)})
		#...
		#_apiGetNeed()
		#core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		core.sendAnswer(conn, "400 Bad Request")
	else:
		core.sendAnswer(conn, "400 Bad Request")
	return True


def handleApiNeeds(conn, method, addr, data):
	if (method == "GET") or (method == "POST"):
		items = core.db.needs.find().limit(1000)
		answer = "["
		for item in items:
			answer += _needItemToStr(item)
		if answer.endswith(','):
			answer = answer[:-1]
		answer += ']'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/needs must GET or POST")
	return True


def handleApiNeedsCount(conn, method, addr, data):
	if method == "GET":
		_getNeedsCountJson(conn)
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/needsCount must GET")
	return True


def handleMessage(msg):
	return False


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handleHttp, handleMessage))
