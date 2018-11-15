import pymongo

import conf


# ==== init ====

client = pymongo.MongoClient("localhost", 27017)
db = client.mhd_1


# ==== Functions ====

def insert1(obj):
	i = db.projects.insert_one(obj).inserted_id
	log(i)


def findAllProjects():
	for item in db.projects.find():
		print(item)


def findProjects2():
	for item in db.projects.find().limit(2):
		print(item["_id"], item)


def findProjects3():
	for item in db.projects.find().limit(2).skip(1):
		print(item["_id"], item)


def log(s):
	print("["+__name__+"]: ",s)
