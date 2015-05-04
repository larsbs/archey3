@module_register("mpd")
class mpdDisplay(display):
    """
    Displays certain stat about MPD database. If mpd not installed, output
    nothing.
    """
    command_line = "mpc stats --host {arg1} --port {arg2}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.stat = kwargs["args"][0]
        except IndexError:
            self.state.logger.error("Did not get any arguments, require one, the stat to display.")
        self.arg1 = self.state.config.get('mpd', 'host', fallback='localhost')
        self.arg2 = self.state.config.getint('mpd', 'port', fallback=6600)

    def format_output(self, instring):
        lines = instring.split('\n')
        stats = {}
        try:
            stats['artists'] = lines[0].split(':')[1].strip()
            stats['albums'] = lines[1].split(':')[1].strip()
            stats['songs'] = lines[2].split(':')[1].strip()
        # if people don't have mpc installed then return None)
        except:
            self.state.logger.error(
                "Could not parse mpc output, is mpc installed?")
            return
        return ('{statname} in MPD database'.format(statname=self.stat.title()), stats[self.stat])
