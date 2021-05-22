class JobLauncherApplicationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class JenkinsServerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

