import re

from archey3 import Display
from modules import module_register
from functions import color


@module_register('sensor')
class SensorModule(Display):
    command_line = 'sensors {arg1}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        arg_from_conf = self.state.config.get('sensor', 'sensor', fallback='coretemp-*')
        try:
            arg_from_arg = kwargs['args'][0]
        except IndexError:
            self.state.logger.error('Did not get any arguments, require one, the sensor to display.')
            raise
        if arg_from_arg:
            self.arg1 = arg_from_arg
        else:
            self.arg1 = arg_from_conf

    def format_output(self, instring):
        tempinfo = instring.split('\n')[2::4]
        out = []
        for line in tempinfo:
            info = [re.sub('\s\s+', '', line) for line in line.split('  ') if line]
            value = info[1]
            intvalue = int(value[:3])
            if intvalue > 45:
                temp = (color(self.state, 'red') + info[1] + color(self.state, 'clear'))
            elif intvalue in range(30, 45):
                temp = (color(self.state, 'magenta') + info[1] + color(self.state, 'clear'))
            else:
                temp = (color(self.state, 'green') + info[1] + color(self.state, 'clear'))
            out.append((info[0], temp))
        return out
