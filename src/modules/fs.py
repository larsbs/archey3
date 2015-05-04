from archey3 import Display
from modules import module_register


class ArgumentError(Exception):
    def __init__(self, caller, message):
        msg = '{0}: {1}'.format(caller.__class__.__name__, message)
        super().__init__(msg)


@module_register('fs')
class FsModule(Display):
    command_line = 'df -TPh {arg1}'

    conversions = {
        'binary': {
            'K': 2 ** 10,
            'M': 2 ** 20,
            'G': 2 ** 30,
            'T': 2 ** 40,
        },
        'si': {
            'K': 10 ** 3,
            'M': 10 ** 6,
            'G': 10 ** 9,
            'T': 10 ** 12,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.arg1:
            msg = 'Did not any arguments, require one, the fs to display'
            self.state.logger.error(msg)
            raise ArgumentError(self, msg)

    def format_output(self, instring):
        try:
            decimal_point = self.call_command(
                'locale -ck decimal_point').split('\n')[1].split('=')[1].strip('\"')
        except Exception as e:
            self.state.logger.warning('Could not determine locale decimal point,' +
                                      'defaulting to \'.\', failed with error {0}'.format(e))
            decimal_point = '.'
        values = [line for line in instring.split('\n') if line][1].split()
        used = values[3].replace(decimal_point, '.')
        total = values[2].replace(decimal_point, '.')
        fstype = values[1]
        conversion_type = self.state.config.get('fs', 'unit', fallback='si').lower()
        conversions = self.conversions[conversion_type]

        mount = '/root' if self.arg1 == '/' else self.arg1
        title = mount.split('/')[-1].title()

        low = self.state.config.getint('fs', 'low_bound', fallback=40)
        medium = self.state.config.getint('fs', 'medium_bound', fallback=70)

        try:
            # convert to straight float
            used_ = float(used[:-1]) * conversions[used[-1].upper()]
            total_ = float(total[:-1]) * conversions[total[-1].upper()]
            percentage = used_ / total_ * 100
        except Exception as e:
            self.state.logger.error(
                'Could not colorize output, errored with {0}'.format(e))
            return
        else:
            used = self.color_me(used, percentage, low=low, medium=medium)

        if self.state.config.getboolean('fs', 'percentage', fallback=True):
            part = '{used} / {total} ({percentage}%) ({fstype})'.format(used=used, total=total,
                                                                        percentage=int(percentage), fstype=fstype)
        else:
            part = '{used} / {total} ({fstype})'.format(used=used, total=total, fstype=fstype)
        return title, part
