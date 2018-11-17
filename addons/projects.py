import datetime

import core


def insert_project(title, description, investments, goal, status, img):
	post1 = {"title": title, "description": description, "investments": investments, "goal": goal, "status": status, "img": img, "createDate": datetime.datetime.utcnow()}
	core.db.projects.insert(post1)


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

def getPostData(data):
	""" Return list of string POST params
	data - utf-8 string
	"""
	params = data.split("\r\n\r\n")[1]
	return params.split("&")


def getProjectsCountJson(conn, addr):
	count = core.db.projects.find().count()
	answer = '{"projectsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def getProjectsJson(conn, addr):
	items = core.db.projects.find().limit(1000)
	answer = "["
	for item in items:
		answer += projectItemToStr(item)
	if answer.endswith(','):
		answer = answer[:-1]
	answer += ']'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def handle(conn, method, addr, data):
	if handleJson(conn, method, addr, data):
		return True
	return handleHtml(conn, method, addr)


def handleHtml(conn, method, addr):
	if addr.startswith("/api/getProjectCard/"):
		projId = addr[19:]
		projId = bytes(projId, "utf-8").decode("unicode_escape").strip().replace('"','')
		answer = '<div class="divBlock divProjectBlockOk"><h3>'+projId+'</h3>Описание проекта<br/><font color="green">Сделано</font><br/><b>2 000 / 2 000</b></div>'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	return False


def handleJson(conn, method, addr, data):
	""" API Request handler (/api)
	method - GET/POST/PUT/DELETE
	data - utf-8 string
	"""
	if addr.startswith("/api/project/"):
		if method == "GET":
			projId = addr[12:]
			projId = bytes(projId, "utf-8").decode("unicode_escape").strip().replace('"','')
			answer = '{"id": "'+projId+'", "name":"Test"}'
			core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		elif method == "POST":
			params = getPostData(data)
			answer = '['
			for p in params:
				if p == "":
					break
				p = p.split("=")
				if len(p) < 2:
					break
				answer += '{"id": "' + p[0] + '", "name": "' + p[1] + '"},'
			if answer.endswith(","):
				answer = answer[:-1]
			answer += ']'
			core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		else:
			core.sendAnswer(conn, "400 Bad Request")
		return True

	if addr.startswith("/api/getProject/"):
		if method != "GET":
			core.sendAnswer(conn, "400 Bad Request")
			return True
		projId = addr[15:]
		projId = bytes(projId, "utf-8").decode("unicode_escape").strip().replace('"','')
		answer = '{"id": "'+projId+'", "name":"Test"}'
		core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))
		return True
	if addr == "/api/getProjects":
		if method == "GET":
			getProjectsJson(conn, addr)
		elif method == "POST":
			postProjectsJson(conn, addr, data)
		else:
			core.sendAnswer(conn, "400 Bad Request")
		return True
	if addr == "/api/getProjectsCount":
		if method == "GET":
			getProjectsCountJson(conn, addr)
		elif method == "POST":
			postProjectsCountJson(conn, addr)
		else:
			core.sendAnswer(conn, "400 Bad Request")
		return True
	if addr == "/api/getProject":
		core.sendAnswer(conn, "400 Bad Request")
		return True
	return False


def log(s):
	print("["+__name__+"]: "+s)


def postProjectsCountJson(conn, addr):
	count = core.db.projects.find().count()
	answer = '{"projectsCount": '+str(count)+'}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def postProjectsJson(conn, addr, data):
	items = core.db.projects.find().limit(1000)
	answer = "["
	for item in items:
		answer += projectItemToStr(item)
	if answer.endswith(','):
		answer = answer[:-1]
	answer += ']'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def projectItemToStr(item):
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


core.addAddon(core.Addon(__name__, handle))
