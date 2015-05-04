import collections

from archey3 import Display
from modules import module_register


DE_DICT = collections.OrderedDict(
    [
        ('cinnamon', 'Cinnamon'),
        ('gnome-session', 'GNOME'),
        ('ksmserver', 'KDE'),
        ('mate-session', 'MATE'),
        ('xfce4-session', 'Xfce'),
        ('lxsession', 'LXDE'),
        ('', 'None'),
    ]
)


@module_register('de')
class DeModule(Display):
    def render(self):
        if self.state.config.get('de', 'manual', fallback=False):
            return "DE", self.state.config.get('de', 'manual')
        de = ''
        for key in DE_DICT.keys():
            if self.process_exists(key):
                de = key
                break
        return 'DE', DE_DICT[de]
