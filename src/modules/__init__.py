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
