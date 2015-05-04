from display import Display


@module_register("ram")
class RamDisplay(Display):
    command_line = "free -m"

    def format_output(self, instring):
        ram = ''.join(line for line in str(instring).split('\n') if line.startswith('Mem:')).split()
        used = int(ram[2])
        total = int(ram[1])
        title = 'RAM'
        try:
            percentage = (used / total * 100)
        except:
            used += ' MB'
        else:
            used = self.color_me(number=percentage, output=str(used) + ' MB')
        part = '{used} / {total} MB'.format(used=used, total=total)
        return title, part