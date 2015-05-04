import os
import re
import configparser
import collections


UNAME_FLAG_MEANINGS = {
    'a': 'System Infomation',
    's': 'Kernel Name',
    'n': 'Hostname',
    'r': 'Kernel Release',
    'v': 'Kernel Version',
    'm': 'Machine Hardware name',
    'p': 'Processor Type',
    'i': 'Hardware Platform',
}


LOGOS = {
    'Arch Linux':
    '''
    {c1}
    {c1}               +                {results[0]}
    {c1}               #                {results[1]}
    {c1}              ###               {results[2]}
    {c1}             #####              {results[3]}
    {c1}             ######             {results[4]}
    {c1}            ; #####;            {results[5]}
    {c1}           +##.#####            {results[6]}
    {c1}          +##########           {results[7]}
    {c1}         ######{c2}#####{c1}##;         {results[8]}
    {c1}        ###{c2}############{c1}+        {results[9]}
    {c1}       #{c2}######   #######        {results[10]}
    {c2}     .######;     ;###;`\".      {results[11]}
    {c2}    .#######;     ;#####.       {results[12]}
    {c2}    #########.   .########`     {results[13]}
    {c2}   ######'           '######    {results[14]}
    {c2}  ;####                 ####;   {results[15]}
    {c2}  ##'                     '##   {results[16]}
    {c2} #'                         `#  {results[17]}
    \x1b[0m
    '''
}


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


COLORS = {
    'black': '0',
    'red': '1',
    'green': '2',
    'yellow': '3',
    'blue': '4',
    'magenta': '5',
    'cyan': '6',
    'white': '7'
}


class ArcheyConfigParser(configparser.SafeConfigParser):
    """
    A parser for the archey config file.
    """
    defaults = {
        'core': {
            'align': 'top',
            'color': 'blue',
            'display_modules': """\
                               distro(), uname(n), uname(r), uptime(), wm(), de(), packages(), ram(),\
                               cpu(), env(editor), fs(/), mpd(albums)
                               """
        },
    }

    def read(self, file_location=None):
        """
        Loads the config options stored in at file_location. If file_location
        does not exist, it will attempt to load from the default config location
        ($XDG_CONFIG_HOME/archey3.cfg). If that does not exist, it will write a
        default config file to $XDG_CONFIG_HOME/archey3.cfg.
        """
        if file_location is None and "XDG_CONFIG_HOME" not in os.environ:
            config_location = os.path.expanduser("~/.archey3.cfg")
        elif file_location is None:
            config_location = os.path.expandvars("$XDG_CONFIG_HOME/archey3.cfg")
        else:
            config_location = os.path.expandvars(os.path.expanduser(file_location))
        loaded = super(ArcheyConfigParser, self).read(config_location)
        if file_location is None and not loaded:
            self.load_default_config()
            self.write_config(config_location)
            return [config_location]
        if not loaded:
            # Try with default
            loaded = super(ArcheyConfigParser, self).read()
        return loaded

    def load_default_config(self):
        """
        Loads the config options stored at self.defaults.
        """
        for section, values in self.defaults.items():
            if not self.has_section(section):
                self.add_section(section)
            for option, value in values.items():
                # Strip any excess spaces
                value = re.sub("( +)", " ", value)
                self.set(section, option, value)

    def write_config(self, location):
        """
        Writes the current config to the given location.
        """
        with open(location, 'w') as configfile:
            self.write(configfile)
