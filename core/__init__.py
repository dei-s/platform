from . import addon
from . import core

Addon = addon.Addon
ObjectId = core.db_mongo.ObjectId

addons = core.addons
addAddon = core.addAddon
config = core.config
db = core.db_mongo.db
handleRecv = core.handleRecv
sendAnswer = core.sendAnswer
sendAnswerFile = core.sendAnswerFile
version = core.version
