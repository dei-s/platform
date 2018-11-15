from . import addon
from . import core

Addon = addon.Addon;
addons = {}

def addAddon(addon):
	addons[addon.name] = addon

config = core.config
db = core.db_mongo.db
sendAnswer = core.sendAnswer
sendAnswerFile = core.sendAnswerFile
version = core.version
