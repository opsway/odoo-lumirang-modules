import logging
import os
from datetime import datetime
from queue import Queue, Empty
from socket import gethostname

from odoo.netsvc import DBFormatter
from requests import post

try:
    import newrelic.agent
except ImportError:
    newrelic = None


def is_a_tty(stream):
    return hasattr(stream, 'fileno') and os.isatty(stream.fileno())


def init_logging(log_level: int, license_key: str,
                 fmt='%(asctime)s %(pid)s %(levelname)s %(dbname)s %(name)s: %(message)s %(perf_info)s'):
    handler = NewRelicHandler(log_level, license_key)
    formatter = DBFormatter(fmt)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


# TODO: use lock to sync threads
class NewRelicHandler(logging.StreamHandler):
    def __init__(self, log_level: int, license_key: str, submit_timeout: float = 60.0, submit_size: int = 5,
                 endpoint: str = "https://log-api.newrelic.com/log/v1", stream=None):
        super().__init__(stream)
        self.log_level = log_level
        self.license_key = license_key
        self.last_submit = datetime.now().timestamp()
        self.submit_timeout = submit_timeout
        self.submit_size = submit_size
        self.records = Queue()
        self.endpoint = endpoint
        app = newrelic.agent.application()
        self.app_name = app.name

    def emit(self, record):
        if record.levelno > self.log_level:
            return
        self.records.put(self.prepare_message(record))
        self._submit()

    def prepare_message(self, record):
        return {
            'timestamp': record.created,
            'message': self.format(record),
            'hostname': gethostname(),
            'service': self.app_name,
            'attributes': {
                'level': record.levelname,
                'process': record.processName,
                'name': record.name,
            }
        }

    def _submit(self):
        if self.records.qsize() < self.submit_size or (
                datetime.now().timestamp() - self.submit_timeout) < self.last_submit:
            return
        records = []
        try:
            records.append(self.records.get_nowait())
        except Empty:
            pass
        post(self.endpoint, json=[{
            'logs': records,
        }], headers={
            'X-License-Key': self.license_key,
        })
