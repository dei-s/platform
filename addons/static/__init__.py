import core
from . import static

core.addAddon(core.Addon(__name__, static.handle))
