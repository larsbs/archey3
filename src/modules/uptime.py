from archey3 import Display
from modules import module_register


@module_register('uptime')
class UptimeModule(Display):
    def render(self):
        with open('/proc/uptime') as upfile:
            raw = upfile.read()
            fuptime = int(raw.split('.')[0])
            day = int(fuptime / 86400)
            fuptime = fuptime % 86400
            hour = int(fuptime / 3600)
            fuptime = fuptime % 3600
            minute = int(fuptime / 60)
            uptime = '{daystring}{hours}:{mins:02d}'.format(
                daystring='{days} day{s}, '.format(days=day, s=('s' if day > 1 else '')) if day
                else '', hours=hour, mins=minute)
            return 'Uptime', uptime
