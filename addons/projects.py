import datetime

import core


def insert_project(title, description, investments, goal, status, img):
	post1 = {"title": title, "description": description, "investments": investments, "goal": goal, "status": status, "img": img, "createDate": datetime.datetime.utcnow()}
	return core.db.projects.insert(post1)


class Project:
	def insert(self):
		insert_project(self.title, self.description, self.investments, self.goal, self.status, self.img);
	def __init__(self, id=0, title="", description="", investments=0, goal=0, status=100, img="", createDate=0):
		self.id = id                    # ObjectId, _id in mongo
		self.title = title
		self.description = description
		self.investments = investments
		self.goal = goal
		self.status = status
		self.img = img
		self.createDate = createDate


# ==== Functions ====

def _apiGetProject(conn, projId):
	projId = bytes(projId, "utf-8").decode("unicode_escape").strip().replace('"','')
	item = core.db.projects.find_one({"_id": core.ObjectId(projId)})
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


def _getProjectsCountJson(conn, addr):
	count = core.db.projects.find().count()
	answer = '{"projectsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def _postProjectsCountJson(conn, addr):
	count = core.db.projects.find().count()
	answer = '{"projectsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def _projectItemToStr(item):
	s = '{"id":"'+str(item["_id"])+'",'
	if 'title' in item:
		s += '"title":"'+str(item["title"]).replace('"','')+'",'
	if 'description' in item:
		s += '"description":'+str(item["description"]).replace('"','')+'",'
	if 'investments' in item:
		s += '"investments":"'+str(item["investments"]).replace('"','')+'",'
	if 'goal' in item:
		s += '"goal":"'+str(item["goal"]).replace('"','')+'",'
	if 'status' in item:
		s += '"status":"'+str(item["status"]).replace('"','')+'",'
	if 'img' in item:
		s += '"img":"'+str(item["img"]).replace('"','')+'",'
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
	if addr.startswith("/api/project"):
		return handleApiProject(conn, method, addr, data)
	if addr.startswith("/api/getProject/"):
		return handleApiGetProject(conn, method, addr, data)
	if addr == "/api/getProjects":
		return handleApiGetProjects(conn, method, addr, data)
	if addr == "/api/getProjectsCount":
		return handleApiGetProjectsCount(conn, method, addr, data)
	if addr.startswith("/api/getProjectCard/"):
		return handleApiGetProjectCard(conn, method, addr, data)
	if addr == "/api/getProject":
		core.sendAnswer(conn, "400 Bad Request")
		return True
	return False


def handleApiGetProject(conn, method, addr, data):
	if method != "GET":
		core.sendAnswer(conn, "400 Bad Request")
		return True
	_apiGetProject(conn, addr[15:])
	return True


def handleApiGetProjectCard(conn, method, addr, data):
	projId = addr[19:]
	projId = bytes(projId, "utf-8").decode("unicode_escape").strip().replace('"','')
	answer = '<div class="divBlock divProjectBlockOk"><h3>'+projId+'</h3>Описание проекта<br/><font color="green">Сделано</font><br/><b>2 000 / 2 000</b></div>'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	return True


def handleApiGetProjects(conn, method, addr, data):
	if (method == "GET") or (method == "POST"):
		items = core.db.projects.find().limit(1000)
		answer = "["
		for item in items:
			answer += _projectItemToStr(item)
		if answer.endswith(','):
			answer = answer[:-1]
		answer += ']'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
	else:
		core.sendAnswer(conn, "400 Bad Request")
	return True


def handleApiGetProjectsCount(conn, method, addr, data):
	if method == "GET":
		_getProjectsCountJson(conn, addr)
	elif method == "POST":
		_postProjectsCountJson(conn, addr)
	else:
		core.sendAnswer(conn, "400 Bad Request")
	return True


def handleApiProject(conn, method, addr, data):
	if method == "GET":
		# Возвращает информацию о проекте в формате JSON
		_apiGetProject(conn, addr[13:])
	elif method == "POST":
		log("handleApiProject POST "+addr)
		# Добавляет новый проект. Если указан id то возвращает ошибку 400.
		params = _getPostData(data)
		pId = addr[13:]
		if pId != "":
			core.sendAnswer(conn, "400 Bad Request")
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
				core.sendAnswer(conn, "400 Bad Request")
				return True
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
		pId = insert_project(pTitle, pDescription, pInvestments, pGoal, pStatus, pImg)
		item = core.db.projects.find_one({"_id": core.ObjectId(pId)})
		if item == None:
			answer = '{}'
		else:
			answer = str(item)
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	elif method == "PUT":
		core.sendAnswer(conn, "400 Bad Request")
	else:
		core.sendAnswer(conn, "400 Bad Request")
	return True


def log(s):
	print("["+__name__+"]: "+s)


core.addAddon(core.Addon(__name__, handle))
