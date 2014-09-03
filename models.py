import mimetypes
import os.path
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from mutagen.mp3 import MP3
from storage import PrivateStorage


APP_NAME = 'podcast'


class Podcast(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    media_url = models.URLField()
    app_root_url = models.URLField()
    favicon = models.ImageField(upload_to='images', blank=True)
    logo_horizontal = models.ImageField(upload_to='images', blank=True)
    itunes_url = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    twitter_hashtag = models.CharField(max_length=100, blank=True)
    twitter_timeline_widget_id = models.CharField(max_length=30, blank=True)
    facebook_app_id = models.CharField(max_length=30, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME


class Episode(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='episode', blank=True)
    pub_date = models.DateTimeField('published_time')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        date = self.pub_date
        if self.slug == '':
            self.slug = '%i-%02d-%02d' % (date.year, date.month, date.day)
        super(Episode, self).save(*args, **kwargs)

    def get_duration(self):
        a_file = MP3(os.path.join(settings.MEDIA_ROOT, self.audio_file.name))
        sec = a_file.info.length
        return '%d:%02d' % (sec // 60, sec % 60)

    def get_mime_type(self):
        return mimetypes.guess_type(self.audio_file.name)[0]

    def get_absolute_url(self):
        return '/podcast/episode/%s' % self.slug

    class Meta:
        app_label = APP_NAME


class ScheduledEpisode(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    slug_base = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='episode', storage=PrivateStorage(), blank=True)
    pub_date = models.DateTimeField('published_time')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            if self.slug_base == '':
                date = self.pub_date
                self.slug = '%i-%02d-%02d' % (date.year, date.month, date.day)
            else:
                self.slug = slugify(self.slug_base)
        super(ScheduledEpisode, self).save(*args, **kwargs)

    class Meta:
        app_label = APP_NAME


class Presenter(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    thumbnail_square = models.ImageField(upload_to='images', blank=True)
    display_order = models.IntegerField(blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    facebook_page = models.URLField(blank=True)
    personal_site = models.URLField(blank=True)
    visibility = models.CharField(max_length=20,
                                  choices=[('visible', 'visible'), ('hidden', 'hidden')],
                                  default='visible')

    class Meta:
        app_label = APP_NAME
        ordering = ['display_order']

    def __unicode__(self):
        return '[%s] %s' % (self.visibility, self.name)

    def save(self, *args, **kwargs):
        if self.display_order is None:
            self.display_order = 999
        super(Presenter, self).save(*args, **kwargs)


class Statement(models.Model):
    unique_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    statement = models.TextField()

    def __unicode__(self):
        return self.unique_name

    class Meta:
        app_label = APP_NAME


class ITunesInfo(models.Model):
    """
    channel(podcast global, not episode-to-episode) attributes passed to iTunes through the "itunes:" tags in RSS
    """
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    subcategory = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    explicit = models.CharField(max_length=100,
                                choices=[('yes', 'yes'), ('clean', 'clean')],
                                default='clean',
                                blank=True)
    owner_name = models.CharField(max_length=100, blank=True)
    owner_email = models.EmailField(blank=True)
    subtitle = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    keywords = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return 'iTunesInfo'

    class Meta:
        app_label = APP_NAME
