import json
import logging
from os import path
from typing import Dict

log = logging.getLogger(__name__)


JSON_REPORT = 'job_launcher_result.json'


def dump_json_report(data: Dict, output: str):
    with open(path.join(output, JSON_REPORT), 'w') as f:
        json.dump(data, f, indent=2)


class Reporter:
    HTML_REPORT = 'job_launcher_result.html'

    def __init__(self, output: str):
        self.json_report_file = path.join(output, JSON_REPORT)
        self.html_report_file = path.join(output, self.HTML_REPORT)

    def generate(self):
        log.info('Start report generation')
        json_report = self._load_json_report()
        message = self._get_message(
            json_report.get('server'),
            json_report.get('results')
        )
        log.info(message)
        log.info('Finish report generation')

    def _load_json_report(self):
        with open(self.json_report_file) as f:
            return json.load(f)

    def _get_message(self, server, results=None):
        results = results or []
        message = [f'Jenkins server: {server}']
        for result in results:
            message.append(f'name: {result.get("name")}')
            message.append(f'status: {result.get("status")}')
            message.append(f'timestamp: {result.get("result", {}).get("timestamp") or "-"}')
            message.append(f'number: {result.get("result", {}).get("number") or "-"}')
            message.append('')
        return '\n'.join(message)

