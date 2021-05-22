import json
import logging
from os import path

from jinja2 import Environment, PackageLoader, select_autoescape

import job_launcher
from job_launcher.api import InitialData

log = logging.getLogger(__name__)


class Reporter:
    TEMPLATES_DIR = 'resources/templates'

    def __init__(self, data: InitialData):
        self.json_report_file = path.join(data.args['output'], data.args['json_report'])
        self.html_report_file = path.join(data.args['output'], data.args['html_report'])
        environment = Environment(
            loader=PackageLoader(job_launcher.__name__, self.TEMPLATES_DIR),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template = environment.get_template('report.html')

    def generate(self):
        log.info('Start report generation')
        json_report = self._load_json_report()
        html_report = self.template.render(**json_report)
        self._dump(html_report)
        log.info('Finish report generation')

    def _load_json_report(self):
        with open(self.json_report_file) as f:
            return json.load(f)

    def _dump(self, html_report: str):
        with open(self.html_report_file, 'w') as f:
            f.write(html_report)


