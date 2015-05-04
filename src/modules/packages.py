from archey3 import Display
from modules import module_register


@module_register('packages')
class PackageModule(Display):
    command_line = 'pacman -Q'

    def format_output(self, instring):
        return 'Packages', len(instring.rstrip('\n').split('\n'))
