import datetime

import core


def _apiGetDream(conn, dreamId):
	dreamId = bytes(dreamId, "utf-8").decode("unicode_escape").strip().replace('"','')
	if dreamId == "":
		core.sendAnswer(conn, "400 Bad Request: dreamId is empty")
		return True
	try:
		item = core.db.dreams.find_one({"_id": core.ObjectId(dreamId)})
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


def _getDreamsCountJson(conn, addr):
	count = core.db.dreams.find().count()
	answer = '{"dreamsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def _insertDream(title, description):
	post1 = {"title": title, "description": description, "createDate": datetime.datetime.utcnow()}
	return core.db.dreams.insert(post1)


def _dreamItemToStr(item):
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


def handle(conn, method, addr, data):
	""" API Request handler (/api)
	method - GET/POST/PUT/DELETE
	data - utf-8 string
	"""
	if (addr == "/api/dream") or addr.startswith("/api/dream/"):
		return handleApiDream(conn, method, addr, data)
	if addr.startswith("/api/getDream?"):
		return handleApiGetDream(conn, method, addr, data)
	if addr == "/api/dreams":
		return handleApiGetDreams(conn, method, addr, data)
	if addr == "/api/getDreams":
		return handleApiGetDreams(conn, method, addr, data)
	if (addr == "/api/dreamsCount") or addr == "/api/getDreamsCount":
		return handleApiGetDreamsCount(conn, method, addr, data)
	if addr.startswith("/api/getDreamCard/") or addr.startswith("/api/getDreamCard?"):
		return handleApiGetDreamCard(conn, method, addr, data)
	if addr == "/api/getDream":
		core.sendAnswer(conn, "400 Bad Request in Dreams addon")
		return True
	return False


def handleApiGetDream(conn, method, addr, data):
	if method != "GET":
		core.sendAnswer(conn, "400 Bad Request: /api/getDream must is GET")
		return True
	_apiGetDream(conn, addr[17:])
	return True


def handleApiGetDreamCard(conn, method, addr, data):
	dreamId = addr[19:]
	dreamId = bytes(dreamId, "utf-8").decode("unicode_escape").strip().replace('"','')
	answer = '<div class="s-dream-div"><h3>'+dreamId+'</h3><p>Dream1</p></div>'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleApiGetDreams(conn, method, addr, data):
	if (method == "GET") or (method == "POST"):
		items = core.db.dreams.find().limit(1000)
		answer = "["
		for item in items:
			answer += _dreamItemToStr(item)
		if answer.endswith(','):
			answer = answer[:-1]
		answer += ']'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/getDreams must GET or POST")
	return True


def handleApiGetDreamsCount(conn, method, addr, data):
	if method == "GET":
		_getDreamsCountJson(conn, addr)
	else:
		core.sendAnswer(conn, "400 Bad Request: /api/getDreamsCount must GET")
	return True


def handleApiDream(conn, method, addr, data):
	if method == "GET":
		# Возвращает информацию о проекте в формате JSON
		_apiGetDream(conn, addr[11:])
	elif method == "POST":
		# Добавляет новый проект. Если указан id то возвращает ошибку 400.
		params = _getPostData(data)
		dreamId = addr[13:]
		if dreamId != "":
			core.sendAnswer(conn, "400 Bad Request: POST /api/dream/xxxx ID is not empty")
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
				core.sendAnswer(conn, "400 Bad Request: POST /api/dream/ ID is not empty")
				return True
			if p[0] == 'title':
				pTitle = p[1]
			if p[0] == 'description':
				pDescription = p[1]
			par[p[0]] = p[1]
		dreamId = _insertDream(pTitle, pDescription)
		item = core.db.dreams.find_one({"_id": core.ObjectId(dreamId)})
		if item == None:
			answer = '{}'
		else:
			answer = str(item)
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	elif method == "PUT":
		# Если указан id то обновляет информацию о проекте в формате JSON иначе возвращает ошибку 400
		params = _getPostData(data)
		dreamId = 0
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
		if dreamId == 0:
			core.sendAnswer(conn, "400 Bad Request: PUT /api/dream/ ID is empty")
			return True
		#item = core.db.dreams.find_one({"_id": core.ObjectId(dreamId)})
		#...
		#_apiGetDream()
		#core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		core.sendAnswer(conn, "400 Bad Request")
	else:
		core.sendAnswer(conn, "400 Bad Request")
	return True


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handle))
