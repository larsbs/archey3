MODULES = {}


def module_register(name):
    """
    Registers the modules classes in the MODULES global.
    """
    def decorator(module):
        MODULES[name] = module
        return module
    return decorator


def setup():
    from modules.process import ProcessCheck
    from modules.distro import DistroCheck
    from modules.cpu import CpuModule
    from modules.ram import RamModule
    # from modules.de import DeModule
    from modules.fs import FsModule
    # from modules.mpd import MpdModule
    from modules.packages import PackageModule
    # from modules.sensor import SensorModule
    from modules.system_upgrade import SystemUpgradeModule
    from modules.uname import UnameModule
    from modules.uptime import UptimeModule
    from modules.wm import WmModule
