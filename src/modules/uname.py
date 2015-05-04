from archey3 import Display
from modules import module_register


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


@module_register('uname')
class UnameModule(Display):
    command_line = 'uname {arg1}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            flag = kwargs['args'][0]
        except IndexError:
            self.state.logger.error('Did not get any arguments, require one, the flag to pass to uname')
            raise
        arg_from_conf = self.state.config.get('uname', 'argument', fallback='')
        arg_from_arg = flag
        if arg_from_arg:
            self.arg1 = '-' + arg_from_arg
        elif arg_from_conf:
            self.arg1 = '-' + arg_from_conf
        else:
            self.arg1 = ''

    def format_output(self, instring):
        return (UNAME_FLAG_MEANINGS[self.arg1[1]], instring)
