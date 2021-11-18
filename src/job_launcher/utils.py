import os

from job_launcher.config import log


def makedirs(directory: str):
    try:
        os.makedirs(directory)
    except FileExistsError:
        log.debug(f"Directory already exist: '{directory}'")