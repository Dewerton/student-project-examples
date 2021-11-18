import json
import logging

from job_launcher.config import LauncherConfig, BuildConfig
from job_launcher.exceptions import JenkinsServerException
from job_launcher.jenkins import JenkinsServer, JenkinsBuild
from job_launcher.report import dump_json_report

log = logging.getLogger(__name__)


class JobLauncher:
    def __init__(self, output: str, config: LauncherConfig):
        self.jenkins = JenkinsServer(config.server, config.user, config.password)
        self.builds = config.builds
        self.result = JobLauncherResult(config.server, output)

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

    def __init__(self, server: str, output: str):
        self.server = server
        self.output = output
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
        dump_json_report(
            {
                'server': self.server,
                'results': self.results,
            },
            self.output
        )
