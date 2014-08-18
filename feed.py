from django.contrib.syndication.views import Feed
from models import Episode, Podcast
from urlparse import urljoin
import mimetypes


class AllEpisodesFeed(Feed):
    podcast = Podcast.objects.get(pk=1)
    if podcast:
        title = podcast.name
        link = '/podcast/feed/'
        description = podcast.description

    def items(self):
        return Episode.objects.all().order_by('-pub_date')

    def item_title(self, episode):
        return episode.title

    def item_pubdate(self, episode):
        return episode.pub_date

    def item_description(self, episode):
        return episode.description + '<h3>Show Notes</h3>' + episode.show_notes

    def item_enclosure_url(self, episode):
        return urljoin(self.podcast.domain, 'media/{0}'.format(episode.audio_file.name))

    def item_enclosure_length(self, episode):
        return episode.audio_file.size

    def item_enclosure_mime_type(self, episode):
        return mimetypes.guess_type(episode.audio_file.name)
