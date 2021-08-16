import re

from setuptools import setup, find_packages
from os import path

HERE = path.abspath(path.dirname(__file__))


def readfile(*parts):
    with open(path.join(HERE, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = readfile(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


setup(
    name='job-launcher',
    version=find_version('src', 'job_launcher', '__init__.py'),
    description='Jenkins jobs launching tool',
    url='https://git.netcracker.com/dmpa1117/everything/tree/job_launcher',
    author='Dmitrii Padozhnikov',
    author_email='dmitrii.padozhnikov@netcracker.com',
    license='Proprietary License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux'
    ],
    packages=find_packages(where='src', include=('job_launcher*',)),
    package_dir={'job_launcher': 'src/job_launcher'},
    python_requires='>=3.6',
    install_requires=[
        'pyyaml>=5.3.1,<6',
        'jenkinsapi>=0.3.11,<0.4',
        'requests>=2.25.1,<3',
        'jinja2==2.11.3',
    ],
    entry_points={
        'console_scripts': [
            'job-launcher = job_launcher.main:main'
        ]
    }
)
