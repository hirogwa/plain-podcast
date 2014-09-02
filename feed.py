from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from models import Episode, Podcast, ITunesInfo
from urlparse import urljoin
import mimetypes


class ITunesFeed(Rss201rev2Feed):
    def rss_attributes(self):
        attrs = super(ITunesFeed, self).rss_attributes()
        attrs.update({"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
        return attrs

    def add_root_elements(self, handler):
        super(ITunesFeed, self).add_root_elements(handler)
        podcast = Podcast.objects.all()[0]
        itunes_info_list = ITunesInfo.objects.all()
        handler.startElement('custom', {})
        handler.startElement('child1', {})
        handler.endElement('child1')
        handler.startElement('child2', {})
        handler.endElement('child2')
        handler.endElement('custom')
        if len(itunes_info_list) > 0:
            itunes_info = itunes_info_list[0]
            handler.addQuickElement('itunes:author', itunes_info.author)
            handler.addQuickElement('itunes:category', attrs={'text': itunes_info.category})
            handler.addQuickElement('itunes:image', attrs={'href': urljoin(podcast.media_url + '/', itunes_info.image.name)})
            handler.addQuickElement('itunes:explicit', itunes_info.explicit)
            handler.addQuickElement('itunes:subtitle', itunes_info.subtitle)
            handler.addQuickElement('itunes:summary', itunes_info.summary)
            handler.addQuickElement('itunes:keywords', itunes_info.keywords)

            # (nested) owner information
            handler.startElement('itunes:owner', {})
            handler.startElement('itunes:name', {})
            handler.characters(itunes_info.owner_name)
            handler.endElement('itunes:name')
            handler.startElement('itunes:email', {})
            handler.characters(itunes_info.owner_email)
            handler.endElement('itunes:email')
            handler.endElement('itunes:owner')

    def add_item_elements(self, handler, item):
        super(ITunesFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('itunes:duration', item['duration'])
        handler.addQuickElement('itunes:explicit', item['explicit'])
        handler.addQuickElement('itunes:subtitle', item['subtitle'])
        handler.addQuickElement('itunes:summary', item['summary'])


class AllEpisodesFeed(Feed):
    feed_type = ITunesFeed
    podcast_list = Podcast.objects.all()
    if len(podcast_list) > 0:
        podcast = podcast_list[0]
        title = podcast.name
        link = '/podcast/feed/'
        description = podcast.description

    itunes_info_list = ITunesInfo.objects.all()
    if len(itunes_info_list) > 0:
        itunes_info = itunes_info_list[0]
    else:
        itunes_info = None

    def items(self):
        return Episode.objects.all().order_by('-pub_date')

    def item_title(self, episode):
        return episode.title

    def item_pubdate(self, episode):
        return episode.pub_date

    def item_description(self, episode):
        return episode.description + '<h3>Show Notes</h3>' + episode.show_notes

    def item_enclosure_url(self, episode):
        return urljoin(self.podcast.media_url + '/', episode.audio_file.name)

    def item_enclosure_length(self, episode):
        return episode.audio_file.size

    def item_enclosure_mime_type(self, episode):
        return mimetypes.guess_type(episode.audio_file.name)[0]

    def item_extra_kwargs(self, episode):
        return {'duration': str(episode.get_duration()),
                'explicit': '' if self.itunes_info is None else self.itunes_info.explicit,
                'subtitle': episode.description,
                'summary': episode.description,
                }
