import core
from . import waves


def apiAddressesBalance(conn, addr):
	myAddress = waves.Address(addr)
	bal = myAddress.balance()
	bal10 = myAddress.balance(confirmations = 10)
	bal20 = myAddress.balance(confirmations = 20)
	mir = myAddress.balance('HdPJha3Ekn1RUR2K9RrY7SG9xK1b21AHPwkL8pcwTmSZ')
	deip = myAddress.balance('8Wj49jM8y9qfFx2QG6HxQXbiaxdnTt8EGm8mEqXJWFL4')
	libre = myAddress.balance('8qqoeygkNFqSjqf8JrB1LtzkCPTS3zJPe3LHDotTJvdH')
	libreMoney = myAddress.balance('9mjqiLEjDD3U1Q4CXTGtqitDGqC84QChkuEUp2TLBjCW')
	answer = '{"address":'+str(addr)
	answer += ',"balance":'+str(bal)
	answer += ',"balance10":'+str(bal10)
	answer += ',"balance20":'+str(bal20)
	answer += ',"mir":'+str(mir)
	answer += ',"deip":'+str(deip)
	answer += ',"libre":'+str(libre)
	answer += ',"libreMoney":'+str(libreMoney)
	answer += '}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def apiHeight(conn):
	h = waves.height();
	answer = '{"height":"'+str(h)+'"}'
	core.sendAnswer(conn, typ="application/json; charset=utf-8", data=answer.encode('utf-8'))


def handleHttp(conn, method, addr, data):
	if (method == "GET") and (addr.startswith("/api/waves/addresses/balance/")):
		apiAddressesBalance(conn, addr[29:], data)
		return True
	if (method == "GET") and (addr == "/api/waves/height"):
		apiHeight(conn)
		return True
	return False


def handleMessage(msg):
	print(__name__, ' v:', msg['v'], ' mt:', msg['mt'], ' of:', msg['of'], ' to:', msg['to'], ' data:', msg['data'])
	if msg['v'] != 1:
		return False
	if msg['mt'] == 'addresses/balance':
		data = msg['data']
		apiAddressesBalance(core.connection['conn'], data['address'])
		return True
	return False
