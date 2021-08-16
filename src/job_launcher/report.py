import json
import logging
from os import path

from job_launcher.data import Arguments

log = logging.getLogger(__name__)


class Reporter:

    def __init__(self, data: Arguments):
        self.json_report_file = path.join(data.output, data.json_report)
        self.html_report_file = path.join(data.output, data.html_report)

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
            message.append(f'timestamp: {result.get("result", {}).get("timestamp", "-")}')
            message.append(f'number: {result.get("result", {}).get("number", "-")}')
            message.append('')
        return '\n'.join(message)

