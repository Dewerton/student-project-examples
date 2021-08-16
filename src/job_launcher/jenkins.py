import logging
import time
from typing import Optional, Dict

from jenkinsapi.build import Build
from jenkinsapi.custom_exceptions import UnknownJob
from jenkinsapi.jenkins import Jenkins, JenkinsAPIException
from requests import RequestException, HTTPError

from job_launcher.exceptions import JobLauncherApplicationException, JenkinsServerException

log = logging.getLogger(__name__)


class JenkinsServer:
    JOB_QUEUE_DELAY = 9  # 9 sec
    JOB_QUEUE_RETRIES = 200  # 9 sec * 200 = 30 min

    JOB_BUILD_DELAY = 30  # 30 sec
    JOB_BUILD_TIMEOUT = 18000  # 18000 sec == 5 hours

    def __init__(self, url: str, username: Optional[str] = None, password: Optional[str] = None):
        self.server_url = url
        try:
            self.server = Jenkins(self.server_url, username, password, timeout=600, useCrumb=True, lazy=True)
        except (RequestException, JenkinsAPIException) as e:
            raise JobLauncherApplicationException(
                f"Failed to connect to Jenkins '{self.server_url}' with user '{username}'. Error: {e.message}"
            ) from e

    def run_job(self, name: str, params: Dict[str, str]) -> 'JenkinsBuild':
        build = self._launch_build(name, params)
        self._wait(build)
        return JenkinsBuild.from_jenkins_api_build(build)

    def _launch_build(self, name: str, params: Dict[str, str]):
        log.info(f"Running the '{name}' job on the '{self.server_url}'")
        try:
            queue_item = self.server[name].invoke(build_params=params)
        except UnknownJob as e:
            raise JenkinsServerException(f"Can't launch job '{name}'") from e
        # implementation mostly copied from QueueItem.block_until_building
        build = None
        for retries_left in reversed(range(self.JOB_QUEUE_RETRIES)):
            try:
                queue_item.poll()
                build = queue_item.get_build()
                break
            except (JenkinsAPIException, HTTPError):
                log.debug(f'Build in queue ({retries_left} retries left) ...')
                time.sleep(self.JOB_QUEUE_DELAY)
        else:
            self.server.get_queue().delete_item(queue_item)
            log.info(f'Queue timeout is over ({self.JOB_QUEUE_RETRIES * self.JOB_QUEUE_DELAY} sec)')
            raise JenkinsServerException('Failed to run the job. Build in queue for too long, timeout is over')
        log.info(f'Build: {build.get_build_url()}')
        return build

    def _wait(self, build: Build) -> None:
        total_wait_time = 0
        while build.is_running() and total_wait_time < self.JOB_BUILD_TIMEOUT:
            time.sleep(self.JOB_BUILD_DELAY)  # 30 sec
            total_wait_time += self.JOB_BUILD_DELAY
            log.debug(f'Build is running for {total_wait_time} sec ...')
        if build.is_running():
            raise JenkinsServerException(f'Build timeout is over ({self.JOB_BUILD_TIMEOUT} sec)')
        build.poll()
        log.info(f'Build status: {build.get_status()}')


class JenkinsBuild:
    def __init__(self, name: str, status, env: dict):
        self.name = name
        self.status = status
        self.env = env

    @classmethod
    def from_jenkins_api_build(cls, build: Build) -> 'JenkinsBuild':
        return cls(
            build.get_build_url(),
            build.get_status(),
            build.get_env_vars()
        )
