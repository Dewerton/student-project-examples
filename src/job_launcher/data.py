from __future__ import annotations

import logging
import os
from collections import namedtuple
from io import TextIOWrapper

import yaml

log = logging.getLogger(__name__)


class LauncherConfig:
    JENKINS_USER_VAR = 'JENKINS_USER'
    JENKINS_PASSWORD_VAR = 'JENKINS_PASSWORD'

    def __init__(self, server, user, password, builds):
        self.server = server
        self.user = user
        self.password = password
        self.builds = builds

    @classmethod
    def parse(cls, yaml_file: TextIOWrapper) -> LauncherConfig:
        config_yaml = yaml.safe_load(yaml_file)
        return cls(
            config_yaml['jenkins_server'],
            os.getenv(cls.JENKINS_USER_VAR),
            os.getenv(cls.JENKINS_PASSWORD_VAR),
            [BuildConfig(build['name'], build['parameters']) for build in config_yaml['builds']]
        )


BuildConfig = namedtuple('BuildConfig', 'job, parameters')
