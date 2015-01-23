import yaml
import sys

configfile = file('plainpodcast.yaml', 'r')
config = yaml.load(configfile)
sys.path.append(config.get('project_directory'))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config.get('project_settings'))

import django
django.setup()

from django.conf import settings
from plainpodcast.models import AccessLog
import logging
import datetime
import os
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('logwatch.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s(%(name)s)%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


LOG_ATTRIBUTES = [
    'remote_addr',
    'remote_user',
    'time_local',
    'request',
    'status',
    'body_bytes_sent',
    'http_referer',
    'http_user_agent',
]

LOG_PATH = config.get('access_log')


class NginxAccessLog():
    @classmethod
    def log_lines(cls, log_path):
        """
        :returns: generator of the lines from the log file
        """
        with open(log_path, 'r') as f:
            for line in f:
                yield line

    @classmethod
    def log_model(cls, logline):
        """
        Converts one line from the log to one AccessLog model.
        :param logline: string that has all the LOG_ATTRIBUTES
            surrounded by double quotations, delimited by \t
        :returns: converted AccessLog model
        """
        params = dict(zip(
            LOG_ATTRIBUTES, [x.strip('" ') for x in logline.split("\t")]))
        params['time_local'] = datetime.datetime.strptime(
            params.get('time_local').split(' ')[0], '%d/%b/%Y:%H:%M:%S')
        return AccessLog(**params)

    @classmethod
    def eatup(cls):
        """
        Converts the contents of the log file to the AccessLog model,
        and archives the log file.
        """
        if not os.path.exists(LOG_PATH):
            logger.info('{} not found. doing nothing'.format(LOG_PATH))
            return

        tgt_path = os.path.normpath(
            '{}_{}'.format(LOG_PATH,
                           datetime.datetime.strftime(
                               datetime.datetime.now(),
                               '%y%m%d%H%M%S')))

        shutil.copyfile(LOG_PATH, tgt_path)
        open(LOG_PATH, 'w').close()

        AccessLog.objects.bulk_create(
            [cls.log_model(x) for x in cls.log_lines(tgt_path)])
        logger.info('{} analyzed and renamed to {}'.format(
            LOG_PATH, tgt_path))


if __name__ == "__main__":
    NginxAccessLog().eatup()
