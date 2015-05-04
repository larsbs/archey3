from datetime import datetime

from archey3 import Display
from modules import module_register


@module_register("system_upgrade")
class SystemUpgradeModule(Display):

    _upgrade_message = 'starting full system upgrade'

    def render(self):
        try:
            datestr = None
            for line in reversed(list(open('/var/log/pacman.log'))):
                if line.rstrip().endswith(self._upgrade_message):
                    datestart = line.find('[')
                    dateend = line.find(']')
                    if datestart != -1 and dateend != -1:
                        datestr = line[datestart + 1:dateend]
                    break
        except Exception as err:
            print(err)
        if not datestr:
            datestr = 'Unknown'
        else:
            currenttime = datetime.today()
            updatetime = datetime.strptime(datestr, '%Y-%m-%d %H:%M')
            numdays = (currenttime - updatetime).days
            datestr = '{0} ({1} days ago)'.format(datestr, numdays)
        return 'Last Upgrade', datestr
