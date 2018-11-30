from . import addon
from . import core

Addon = addon.Addon
ObjectId = core.db_mongo.ObjectId

addons = core.addons
addAddon = core.addAddon
config = core.config
connection = core.connection
db = core.db_mongo.db
getHttpData = core.getHttpData
getHttpHeader = core.getHttpHeader
handleMessage = core.handleMessage
handleMessage1 = core.handleMessage1
handleRecv = core.handleRecv
sendAnswer = core.sendAnswer
sendAnswerFile = core.sendAnswerFile
version = core.version
