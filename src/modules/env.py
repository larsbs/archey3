import os

from archey3 import Display
from modules import module_register


@module_register('env')
class EnvModule(Display):
    def __init__(self, **kwargs):
        try:
            self.arg1 = kwargs['args'][0]
        except IndexError:
            self.state.logger.error('Did not get any arguments, require one, the env variable to display.')
            raise
        super().__init__(**kwargs)

    def render(self):
        argvalue = os.getenv(self.arg1.upper())
        return ('$' + self.arg1.upper(), argvalue)
