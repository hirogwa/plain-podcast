import yaml
import sys

configfile = file('plainpodcast.yaml', 'r')
config = yaml.load(configfile)
sys.path.append(config.get('project_directory'))

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config.get('project_settings'))

import django
django.setup()

from plainpodcast.models import ScheduledEpisode, Episode
import datetime
import logging
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler('batch.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s(%(name)s)%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class EpisodeUploader():

    def __init__(self):
        pass

    def execute_all(self):
        logger.info('checking for episodes to upload.')
        scheduled_episodes = ScheduledEpisode.objects.all().order_by(
            'pub_date')
        uploaded_episodes = []
        for ep in scheduled_episodes:
            ep_time = ep.pub_date
            now_time = pytz.utc.localize(datetime.datetime.now())
            if now_time > ep_time:
                logger.info('uploading episode %s' % ep.title)
                self.upload_episode(ep)
                uploaded_episodes.append(ep)
                ep.delete()

        logger.info('%d episodes uploaded.' % len(uploaded_episodes))

    def upload_episode(self, episode):
        new_episode = Episode(title=episode.title,
                              slug=episode.slug,
                              description=episode.description,
                              show_notes=episode.show_notes,
                              audio_file=episode.audio_file,
                              pub_date=episode.pub_date)
        new_episode.save()


if __name__ == '__main__':
    EpisodeUploader().execute_all()
