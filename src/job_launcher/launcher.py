import json
import logging
from os import path

from job_launcher.data import LauncherConfig, BuildConfig, Arguments
from job_launcher.exceptions import JenkinsServerException
from job_launcher.jenkins import JenkinsServer, JenkinsBuild

log = logging.getLogger(__name__)


class JobLauncher:
    def __init__(self, args: Arguments, config: LauncherConfig):
        self.jenkins = JenkinsServer(config.server, config.user, config.password)
        self.builds = config.builds
        self.result = JobLauncherResult(config.server, args)

    def run(self):
        log.info('Start job launcher')
        for build in self.builds:
            try:
                jenkins_build = self.jenkins.run_job(build.job, build.parameters)
            except JenkinsServerException as e:
                log.warning(f"Build launch isn't successful: {e}")
                jenkins_build = self._get_stub_build(build)
            self.result.append(jenkins_build)
        log.info('Dumping report')
        self.result.dump()
        log.info('Finish job launcher')

    def _get_stub_build(self, build: BuildConfig) -> JenkinsBuild:
        return JenkinsBuild(
            f"job: {build.job}, parameters: " + ', '.join([f"{item[0]}={item[1]}" for item in build.parameters.items()]),
            status="UNKNOWN",
            env={}
        )


class JobLauncherResult:
    BUILD_RESULT_ENV = 'BUILD_RESULT'

    def __init__(self, server: str, args: Arguments):
        self.server = server
        self.result_file = path.join(args.output, args.json_report)
        self.results = []

    def append(self, build: JenkinsBuild):
        raw_build_result = build.env.get(self.BUILD_RESULT_ENV, '{}')
        log.debug(raw_build_result)
        build_result = json.loads(raw_build_result)
        build_result.setdefault('timestamp', None)
        build_result.setdefault('number', None)
        self.results.append({
            'name': build.name,
            'status': build.status,
            'result': build_result,
        })

    def dump(self):
        with open(self.result_file, 'w') as f:
            json.dump(
                {
                    'server': self.server,
                    'results': self.results,
                },
                f, indent=2
            )
