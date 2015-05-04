@module_register("packages")
class packageDisplay(display):
    command_line = "pacman -Q"

    def format_output(self, instring):
        return "Packages", len(instring.rstrip('\n').split('\n'))
