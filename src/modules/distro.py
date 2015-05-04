from archey3 import Display
from modules import module_register


@module_register('distro')
class DistroCheck(Display):
    def render(self):
        try:
            open('/etc/pacman.conf')
        except IOError:
            distro = self.call_command('uname -o')
        else:
            distro = 'Arch Linux'
        distro = '{0} {1}'.format(distro, self.call_command('uname -m'))
        return 'OS', distro
