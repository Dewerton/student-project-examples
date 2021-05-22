from __future__ import annotations

import logging
from os import makedirs

from argparse import ArgumentParser, FileType

from job_launcher import __version__ as version

log = logging.getLogger(__name__)


class InitialData:
    def __init__(self, args):
        self.args = args

    def should_run(self):
        return self.args['subparser'] == 'run'

    def should_generate_report(self):
        return self.args['subparser'] == 'report' or (self.args['subparser'] == 'run' and self.args['report'])

    @classmethod
    def init(cls) -> InitialData:
        data = cls._parse()
        cls.init_logger(data.args['debug'])
        data.args['json_report'] = 'job_launcher_result.json'
        data.args['html_report'] = 'job_launcher_result.html'

        cls._makedirs([data.args['output']])
        return data

    @staticmethod
    def init_logger(is_debug: bool):
        logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO)
        logging.getLogger('urllib3').setLevel(logging.INFO)
        logging.getLogger('jenkinsapi').setLevel(logging.INFO)

    @staticmethod
    def _makedirs(dirs: list):
        for directory in dirs:
            try:
                makedirs(directory)
            except FileExistsError:
                log.debug(f"Directory already exist: '{directory}'")

    @classmethod
    def _parse(cls) -> InitialData:
        parser = ArgumentParser(prog='job-launcher')
        parser.add_argument('--version', action='version', version='%(prog)s {}'.format(version))
        parser.add_argument('--debug', action='store_true', help='Activate debug logging')
        parser.add_argument('-o', '--output', default='output', help='Output folder for reports')
        subparsers = parser.add_subparsers(description='', dest='subparser', required=True)

        run_parser = subparsers.add_parser('run', help='run jobs')
        run_parser.add_argument('config', type=FileType('r'), help='a config file')
        run_parser.add_argument('-r', '--report', action='store_true', help='Generate report after jobs run')

        report_parser = subparsers.add_parser('report', help='Generate report from stored data')
        return cls(vars(parser.parse_args()))

