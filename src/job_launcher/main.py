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
        if args.should_run():
            config = LauncherConfig.parse(args.config)
            JobLauncher(args, config).run()
        if args.should_generate_report():
            Reporter(args).generate()
    except JobLauncherApplicationException as e:
        log.error(e)
        sys.exit(1)
    except Exception:
        log.exception('Fatal error occurs')
        sys.exit(2)


if __name__ == '__main__':
    main()
