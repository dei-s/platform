import core
from . import handle
from . import waves


Address = waves.Address;
apiAddressesBalance = handle.apiAddressesBalance
apiHeight = handle.apiHeight


core.addAddon(core.Addon(__name__, handle.handleHttp, handle.handleMessage))
