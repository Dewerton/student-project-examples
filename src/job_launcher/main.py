import logging
import sys

import job_launcher
from job_launcher.api import InitialData
from job_launcher.data import LauncherConfig
from job_launcher.exceptions import JobLauncherApplicationException
from job_launcher.launcher import JobLauncher
from job_launcher.report import Reporter

log = logging.getLogger(job_launcher.__name__)


def main():
    try:
        data = InitialData.init()
        if data.should_run():
            config = LauncherConfig.parse(data.args['config'])
            JobLauncher(data, config).run()
        if data.should_generate_report():
            Reporter(data).generate()
    except JobLauncherApplicationException as e:
        log.error(e)
        sys.exit(1)
    except Exception:
        log.exception('Fatal error occurs')
        sys.exit(2)


if __name__ == '__main__':
    main()
