import sys
import subprocess
import collections
from time import sleep, ctime
from logbook import Logger

from modules import MODULES
from config import COLORS


# State must be serializable
State = collections.namedtuple("State", "color config logger")


def screenshot(state):
    print('Screenshotting in')
    screenshot_time = state.config.getint("core", "screenshotwait", fallback=5)
    for x in sorted(range(1, screenshot_time + 1), reverse=True):
        print('%s' % x, end='')
        sys.stdout.flush()
        sleep(1.0/3)
        for x in range(3):
            print('.', end='')
            sys.stdout.flush()
            sleep(1.0/3)
    print('Say Cheese!')
    sys.stdout.flush()
    screenshot_command = state.config.get('core', 'screenshot_command', fallback="import -window root <datetime>.jpg")
    try:
        subprocess.check_call(
            screenshot_command.replace('<datetime>', ctime().replace(' ', '_')).split(" "))
    except subprocess.CalledProcessError as e:
        state.logger.critical('Screenshot failed with return code {0}.'.format(e.returncode))
        raise
    except subprocess.FileNotFoundError:
        print("Could not find import command, install imagemagick")


def color(state, code, bold=False):
    """
    Returns a character color sequence acording to the code given, and the
    color theme in the state argument.
    """
    if code == 2:
        bold = True
    first_bitty_bit = '\x1b[{0};'.format(int(not bold))
    if code in range(3):
        second_bitty_bit = '3{0}m'.format(state.color)
    elif code == "clear":
        return '\x1b[0m'
    else:
        second_bitty_bit = '3{0}m'.format(COLORS[code])
    return first_bitty_bit + second_bitty_bit


def _mp_render_helper(container):
    """
    A little helper to get round the one iterator argument with
    multiprocessing.Pool.map.
    """
    state = container["state"]
    cls_name = container["cls_name"]
    args = container["args"]
    module = MODULES[cls_name]
    return render_class(state, module, args)


def render_class(state, cls, args):
    """
    Returns the result of the run_command method for the class passed.
    """
    try:
        instance = cls(args=args, state=State(
            logger=Logger(cls.__name__, state.logger.level),
            color=state.color,
            config=state.config)
        )
    except Exception as e:
        state.logger.error("Could not instantiate {0}, failed with error {1}".format(cls.__name__, e))
        return
    try:
        instance.run_command()
        return instance.render()
    except Exception as e:
        state.logger.error("Could not render line for {0}, failed with error {1}".format(cls.__name__, e))


def clean_whitespaces(string):
    """
    Remove all duplicate whitespaces in a string
    and replace them all with a single whitespace.
    """
    return ' '.join(string.split())
