import logging
import sys

import job_launcher
from job_launcher.data import LauncherConfig, initialize
from job_launcher.exceptions import JobLauncherApplicationException
from job_launcher.launcher import JobLauncher
from job_launcher.report import Reporter

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


if __name__ == '__main__':
    main()
