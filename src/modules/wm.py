import re
import collections

from archey3 import Display
from modules import module_register


WM_DICT = collections.OrderedDict(
    [
        ('awesome', 'Awesome'),
        ('beryl', 'Beryl'),
        ('blackbox', 'Blackbox'),
        ('bspwm', 'bspwm'),
        ('dwm', 'DWM'),
        ('enlightenment', 'Enlightenment'),
        ('fluxbox', 'Fluxbox'),
        ('fvwm', 'FVWM'),
        ('herbstluftwm', 'herbstluftwm'),
        ('i3', 'i3'),
        ('icewm', 'IceWM'),
        (re.compile('kwin(_x11|_wayland)?'), 'KWin'),
        ('metacity', 'Metacity'),
        ('musca', 'Musca'),
        ('openbox', 'Openbox'),
        ('pekwm', 'PekWM'),
        ('ratpoison', 'ratpoison'),
        ('scrotwm', 'ScrotWM'),
        ('subtle', 'subtle'),
        ('monsterwm', 'MonsterWM'),
        ('wmaker', 'Window Maker'),
        ('wmfs', 'Wmfs'),
        ('wmii', 'wmii'),
        ('xfwm4', 'Xfwm'),
        ('emerald', 'Emerald'),
        ('compiz', 'Compiz'),
        (re.compile('xmonad-*'), 'xmonad'),
        ('qtile', 'QTile'),
        ('wingo', 'Wingo'),
        ('', 'None'),
    ]
)


@module_register('wm')
class WmModule(Display):
    def render(self):
        if self.state.config.get('wm', 'manual', fallback=False):
            return 'WM', self.state.config.get('wm', 'manual')
        wm = ''
        for key in WM_DICT.keys():
            if self.process_exists(key):
                wm = key
                break
        return 'WM', WM_DICT[wm]
