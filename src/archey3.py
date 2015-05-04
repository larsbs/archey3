#!/usr/bin/env python
#
# archey3 [version 0.5]
#
# Copyright 2010 Melik Manukyan <melik@archlinux.us>
# Copyright 2010-2012 Laurie Clark-Michalek <bluepeppers@archlinux.us>
# Copyright 2015 Lorenzo Ruiz <lars@sindrosoft.com>
# Distributed under the terms of the GNU General Public License v3.
# See http://www.gnu.org/licenses/gpl.txt for the full license text.
#
# Simple python script to display an Archlinux logo in ASCII art
# Along with basic system information.

import re
import subprocess
import multiprocessing
from optparse import OptionParser
from logbook import Logger, lookup_level

import modules
from modules import MODULES
from config import ArcheyConfigParser, COLORS, LOGOS
from functions import State, render_class, _mp_render_helper, color, screenshot


PROCESSES = None


class Display(object):
    command_line = ''
    stdindata = ''
    regex_class = re.compile('').__class__

    def __init__(self, state, args=()):
        self.state = state
        self.arg1, self.arg2, self.arg3, *_ = tuple(args) + ('', '', '')

    @staticmethod
    def call_command(command):
        """
        Calls a command, waits for it to exit and returns all text from stdout.
        Discards all other information.
        """
        proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        proc.wait()
        return proc.communicate()[0].decode()

    def run_command(self):
        if self.command_line:
            if '{arg3}' in self.command_line:
                cmd = self.command_line.format(arg1=self.arg1, arg2=self.arg2, arg3=self.arg3)
            elif '{arg2}' in self.command_line:
                cmd = self.command_line.format(arg1=self.arg1, arg2=self.arg2)
            elif '{arg1}' in self.command_line:
                cmd = self.command_line.format(arg1=self.arg1)
            else:
                cmd = self.command_line

            try:
                self.process = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception:
                self.state.logger.error('Could not run command {0}'.format(cmd))

    def render(self):
        (stdoutdata, stderrdata) = self.process.communicate(self.stdindata or None)
        return self.format_output(stdoutdata.decode())

    def color_me(self, output, number=None, low=30, low_color='green',
                 medium=60, medium_color='yellow', high_color='red'):
        if number is None and output.isdigit():
            number = int(output)
        elif number is None:
            return output

        if number <= low:
            color_ = low_color
        elif low < number <= medium:
            color_ = medium_color
        elif medium < number:
            color_ = high_color

        return '{0}{1}{2}'.format(color(self.state, color_), output, color(self.state, 'clear'))

    def process_exists(self, key):
        global PROCESSES
        if isinstance(key, self.regex_class):
            for proc in PROCESSES._processes:
                if key.search(proc):
                    return True
        return PROCESSES(key)


class Archey(object):
    DISPLAY_PARSING_REGEX = '(?P<func>\w+)\((|(?P<args>[\w, /]+))\)'

    def __init__(self, config, options):
        modules.setup()

        log_level = lookup_level(options.log_level)
        logger = Logger('Core', log_level)

        self.display = config.get('core', 'display_modules')

        colorscheme = options.color or config.get('core', 'color', fallback='blue')
        for key in COLORS.keys():
            if key == colorscheme:
                colorcode = COLORS[key]
        self.state = State(colorcode, config, logger)

        global PROCESSES
        PROCESSES = render_class(self.state, MODULES['process_check'], ())

        distro_out = render_class(self.state, MODULES['distro'], ())
        if not distro_out:
            self.state.logger.critical('Unrecognised distribution.')
            raise RuntimeError('Unrecognised distribution.')
        self.distro_name = ' '.join(distro_out[1].split()[:-1])

    def run(self, take_screenshot=False):
        """
        Actually print the logo etc, and take a screenshot if required.
        """
        print(self.render())
        if take_screenshot:
            screenshot(self.state)

    def render(self):
        results = self.prepare_results()
        results = self.arrange_results(results)
        return LOGOS[self.distro_name].format(c1=color(self.state, 1), c2=color(self.state, 2), results=results)

    def prepare_results(self):
        """
        Renders all classes found in the display array, and then returns them
        as a list. The returned list will be exactly 18 items long, with any
        left over spaces being filled with empty strings.
        """
        poolsize = self.state.config.getint('core', 'poolsize', fallback=5)
        pool = multiprocessing.Pool(poolsize)
        arguments = []
        for cls_name, args in self.parse_display():
            arguments.append({'cls_name': cls_name, 'args': args, 'state': self.state})
        raw_out = pool.map(_mp_render_helper, arguments)
        outputs = list(map(self.format_item, filter(bool, raw_out)))
        return outputs + [""] * (18 - len(outputs))

    def arrange_results(self, results):
        """
        Arranges the results as specified in the config file.
        """
        arrangement = self.state.config.get('core', 'align', fallback='top')
        if arrangement == 'top':
            return results
        elif arrangement == 'bottom':
            actuall_res = [res for res in results if res]
            return [""] * (len(results) - len(actuall_res)) + actuall_res
        elif arrangement == 'center':
            actuall_res = [res for res in results if res]
            offset = [""] * int((len(results) - len(actuall_res)) / 2)
            return (offset + actuall_res + [''] * (len(results) - len(actuall_res)))
        else:
            return results

    def parse_display(self):
        """
        Iterates over the display attribute of the Archey class, and tries to
        parse them using the DISPLAY_PARSING_REGEX.
        """
        for func in self.display.split(","):
            func = func.strip()
            info = re.match(self.DISPLAY_PARSING_REGEX, func)
            if not info:
                self.state.logger.error('Could not parse display string {0}'.format(func))
                continue
            groups = info.groupdict()
            if groups['args']:
                args = [arg.strip() for arg in groups['args'].split(",")]
            else:
                args = ()
            yield groups['func'], args
        raise StopIteration

    def format_item(self, item):
        title = item[0].rstrip(':')
        data = str(item[1]).rstrip()
        # If we're dealing with a fraction
        if len(data.split('/')) == 2:
            numerator = data.split('/')[0]
            numerator = (color(self.state, 1, bold=True) + numerator + color(self.state, 'clear'))
            denominator = data.split('/')[1]
            data = '/'.join((numerator, denominator))
        return '{color}{title}:{clear} {data}'.format(
            color=color(self.state, 1),
            title=title,
            data=data,
            clear=color(self.state, 'clear')
        )


def main():
    parser = OptionParser(
        usage='%prog',
        description="""%prog is a utility to display system info and take screenshots""",
        version="%prog 0.3",
    )
    parser.add_option(
        '-c', '--color',
        action='store', type='choice', dest='color',
        choices=(
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white'
        ),
        help="""choose a color: black, red, green, yellow, blue, magenta, cyan, white [Default: blue]""")
    parser.add_option(
        '-s', '--screenshot',
        action='store_true', dest='screenshot', help='Take a screenshot'
    )
    parser.add_option(
        '--config',
        action='store', dest='config', default=None, help='Set the location of the config file to load.')
    parser.add_option(
        '--debug',
        action='store', type='choice', dest='log_level',
        choices=(
            'NOTSET',
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ),
        default='CRITICAL',
        help='The level of errors you wish to display. Choices are NOTSET, DEBUG, INFO, WARNING, ERROR, and CRITICAL. \
        CRITICAL is the default.'
    )
    (options, args) = parser.parse_args()
    config = ArcheyConfigParser()
    config.read(options.config)
    archey = Archey(config=config, options=options)
    archey.run(options.screenshot)


if __name__ == '__main__':
    main()
