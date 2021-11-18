import logging
import os
from argparse import ArgumentParser, FileType
from collections import namedtuple
from io import TextIOWrapper

import yaml

from job_launcher import __version__ as version
from job_launcher.exceptions import JobLauncherApplicationException

log = logging.getLogger(__name__)


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


def makedirs(directory: str):
    try:
        os.makedirs(directory)
    except FileExistsError:
        log.debug(f"Directory already exist: '{directory}'")


class LauncherConfig:
    JENKINS_USER_VAR = 'JENKINS_USER'
    JENKINS_PASSWORD_VAR = 'JENKINS_PASSWORD'

    def __init__(self, server, user, password, builds):
        self.server = server
        self.user = user
        self.password = password
        self.builds = builds

    @classmethod
    def parse(cls, yaml_file: TextIOWrapper) -> 'LauncherConfig':
        try:
            config_yaml = yaml.safe_load(yaml_file)
            return cls(
                config_yaml['jenkins_server'],
                os.getenv(cls.JENKINS_USER_VAR),
                os.getenv(cls.JENKINS_PASSWORD_VAR),
                [BuildConfig(build['name'], build['parameters']) for build in config_yaml['builds']]
            )
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise JobLauncherApplicationException(e) from e
        except KeyError as e:
            raise JobLauncherApplicationException(f'No such key: {e}') from e


BuildConfig = namedtuple('BuildConfig', 'job, parameters')
