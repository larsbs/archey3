from archey3 import Display
from functions import clean_whitespaces
from modules import module_register


@module_register('cpu')
class CpuModule(Display):
    command_line = 'cat /proc/cpuinfo'

    def format_output(self, instring):
        kv = [line.split(':') for line in instring.split('\n') if line]
        infodict = {}
        for k, v in kv:
            infodict[k.strip()] = v.strip()
        return 'CPU', clean_whitespaces(infodict['model name'])
