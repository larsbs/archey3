from getpass import getuser

from archey3 import Display
from modules import module_register


@module_register("process_check")
class ProcessCheck(Display):
    command_line = "ps -u " + getuser()

    def render(self):
        return self

    def run_command(self):
        super().run_command()
        out = str(self.process.communicate()[0])
        self._processes = set()
        for line in out.split("\\n"):
            words = line.split()
            if len(words) <= 3:
                continue
            self._processes.add(words[3])

    def __call__(self, proc):
        if proc in self._processes:
            return True
        return False
