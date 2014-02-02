import logging
import os

import GreenletProfiler

from nose.plugins.base import Plugin
from nose.util import tolist

logger = logging.getLogger('nose.plugins.nose_greenlet_profiler')

class Profile(Plugin):
    ''' Use this plugin to run tests using the GreenletProfiler profiler. '''

    enabled = True
    name = 'greenlet-profiler'
    score = 0

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.stats_file = 'stats.dat'
        self.stats_type = None

    def options(self, parser, env):
        ''' Register commandline options. '''
        super(Profile, self).options(parser, env)

        parser.add_option('--greenlet-profiler-clock-type', action='store',
                          dest='clock_type',
                          choices=['cpu', 'wall'],
                          default='wall',
                          help='Profiler clock type; default "wall"')

        parser.add_option('--greenlet-profiler-stats-file', action='store',
                          dest='stats_file',
                          metavar="FILE",
                          default=env.get('NOSE_PROFILE_STATS_FILE'),
                          help='Profiler stats file; default "stats.dat"')

        parser.add_option('--greenlet-profiler-stats-print', action='store',
                          dest='stats_print',
                          default=True,
                          help='Print stats')

        parser.add_option("--greenlet-profiler-stats-erase", action="store_true",
                          default=env.get('NOSE_PROFILE_STATS_ERASE'),
                          dest="stats_erase",
                          help="Erase previously-collected profiling statistics before run")

        parser.add_option('--greenlet-profiler-stats-type', action='store',
                          dest='stats_type',
                          choices=['pstat', 'callgrind'],
                          default='pstat',
                          help='Profile stats file type; default "pstats"')


    def configure(self, options, conf):
        super(Profile, self).configure(options, conf)
        self.conf = conf
        logger.debug('configuring with options %r', options)
        logger.debug('configuring with conv %r', conf)

        if options.stats_file: self.stats_file = options.stats_file
        if options.stats_type: self.stats_type = options.stats_type
        self.stats_print = options.stats_print

        if options.stats_erase:
            self._erase_stats_file()

        if options.clock_type:
            GreenletProfiler.set_clock_type(options.clock_type)

    def prepareTest(self, test):
        ''' Wrap entire test run in :func:`prof.runcall`. '''
        logger.debug('preparing test %s' % test)
        def run_and_profile(result):
            GreenletProfiler.start()
            try:
                test(result)
            finally:
                GreenletProfiler.stop()
                self.stats = GreenletProfiler.get_func_stats()

        return run_and_profile

    def report(self, stream):
        logger.debug('printing stats? %d', self.stats_print)
        if not self.stats_print:
            self.stats.print_all(stream)

        logger.debug('dumping stats? %s', self.stats_file)
        if self.stats_file:
            self.stats.save(self.stats_file, type=self.stats_type)

    def _erase_stats_file(self):
        if os.path.exists(self.stats_file):
            os.unlink(self.stats_file)

if __name__ == '__main__':
    nose.main(addplugins=[Profile()])
