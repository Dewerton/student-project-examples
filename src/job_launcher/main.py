import logging
import sys
from argparse import ArgumentParser, FileType

import job_launcher
from job_launcher import __version__ as version
from job_launcher.config import LauncherConfig
from job_launcher.exceptions import JobLauncherApplicationException
from job_launcher.launcher import JobLauncher
from job_launcher.report import Reporter
from job_launcher.utils import makedirs

log = logging.getLogger(job_launcher.__name__)


def main():
    try:
        args = initialize()
        if should_run(args):
            config = LauncherConfig.parse(args.config)
            JobLauncher(args.output, config).run()
        if should_generate_report(args):
            Reporter(args.output).generate()
    except JobLauncherApplicationException as e:
        log.error(e)
        sys.exit(1)
    except Exception:
        log.exception('Fatal error occurs')
        sys.exit(2)


def should_run(args):
    return args.subparser == 'run'


def should_generate_report(args):
    return args.subparser == 'report' or (args.subparser == 'run' and args.report)


def initialize():
    args = parse_arguments()
    init_logger(args.debug)
    makedirs(args.output)
    return args


def parse_arguments():
    parser = ArgumentParser(prog='job-launcher')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(version))
    parser.add_argument('--debug', action='store_true', help='Activate debug logging')
    parser.add_argument('-o', '--output', default='output', help='Output folder for reports')
    subparsers = parser.add_subparsers(description='', dest='subparser')

    run_parser = subparsers.add_parser('run', help='run jobs')
    run_parser.add_argument('config', type=FileType('r'), help='a config file')
    run_parser.add_argument('-r', '--report', action='store_true', help='Generate report after jobs run')

    report_parser = subparsers.add_parser('report', help='Generate report from stored data')
    return parser.parse_args()


def init_logger(is_debug: bool):
    logging.basicConfig(level=logging.DEBUG if is_debug else logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.getLogger('jenkinsapi').setLevel(logging.INFO)


if __name__ == '__main__':
    main()
