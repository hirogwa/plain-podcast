import datetime
import mimetypes
import os
import plainpodcast.settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify
from mutagen.mp3 import MP3

APP_LABEL = 'plainpodcast'


class PodcastModel(models.Model):
    class Meta:
        abstract = True
        app_label = APP_LABEL


class Theme(PodcastModel):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Podcast(PodcastModel):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    theme = models.ForeignKey(Theme)
    media_url = models.URLField()    # TODO remove?
    app_root_url = models.URLField()
    favicon = models.ImageField(upload_to='images', blank=True)
    logo_horizontal = models.ImageField(upload_to='images', blank=True)
    logo_stamp = models.ImageField(upload_to='images', blank=True)
    itunes_url = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    instagram_id = models.CharField(max_length=100, blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    twitter_hashtag = models.CharField(max_length=100, blank=True)
    twitter_timeline_widget_id = models.CharField(max_length=30, blank=True)
    facebook_app_id = models.CharField(max_length=30, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    google_contact_iframe = models.TextField(blank=True)
    disqus_shortname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Episode(PodcastModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='episode')
    duration = models.FloatField(blank=True)
    pub_date = models.DateTimeField('published_time')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        # slug
        date = self.pub_date
        if self.slug == '':
            self.slug = '%i-%02d-%02d' % (date.year, date.month, date.day)

        # duration
        temppath = os.path.join(
            plainpodcast.settings.TEMP_DIR,
            '{}.tmp'.format(os.path.basename(self.audio_file.name)))
        with open(temppath, 'wb') as tempfile:
            tempfile.write(self.audio_file.file.file.getvalue())
        self.duration = MP3(temppath).info.length

        super(Episode, self).save(*args, **kwargs)

    def get_duration(self):
        sec = self.duration
        return '%d:%02d' % (sec // 60, sec % 60)

    def get_mime_type(self):
        return mimetypes.guess_type(self.audio_file.name)[0]

    def get_absolute_url(self):
        return '/%s/episode/%s' % (APP_LABEL, self.slug)


class ScheduledEpisode(PodcastModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    slug_base = models.CharField(max_length=100, blank=True)  # TODO remove
    description = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='episode', blank=True)
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


class Presenter(PodcastModel):
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

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.display_order is None:
            self.display_order = 999
        super(Presenter, self).save(*args, **kwargs)


class Statement(PodcastModel):
    unique_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    statement = models.TextField()

    def __unicode__(self):
        return self.unique_name


class ITunesInfo(PodcastModel):
    """
    channel(podcast global, not episode-to-episode) attributes
    passed to iTunes through the "itunes:" tags in RSS
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


class Promotion(PodcastModel):
    name = models.CharField(max_length=50)
    active = models.CharField(max_length=10,
                              choices=[('active', 'active'),
                                       ('inactive', 'inactive')],
                              default='active')
    image = models.ImageField(upload_to='images', blank=True)
    caption = models.TextField(blank=True)
    caption_location = models.CharField(max_length=50,
                                        choices=[('BL', 'bottom-left'),
                                                 ('BR', 'bottom-right')],
                                        default='BL')
    display_order = models.IntegerField(default=99)
    input_datetime = models.DateTimeField(blank=True)
    update_datetime = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if (not Promotion.objects.filter(id=self.id)) & (not self.input_datetime):
            self.input_datetime = datetime.datetime.now()
        self.update_datetime = datetime.datetime.now()
        super(Promotion, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['display_order', '-input_datetime']
        app_label = APP_LABEL


class Article(PodcastModel):
    title = models.CharField(max_length=100)
    visibility = models.CharField(max_length=50,
                                  choices=[('visible', 'visible'), ('hidden', 'hidden')],
                                  default='visible')
    author = models.ForeignKey(Presenter)
    slug = models.SlugField(blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField('published_time', blank=True)

    def save(self, *args, **kwargs):
        if (not self.__class__.objects.filter(id=self.id)) & (not self.pub_date):
            self.pub_date = datetime.datetime.now()
            date = self.pub_date
            if self.slug == '':
                self.slug = '%i-%02d-%02d-%02d%02d' % (date.year, date.month, date.day, date.hour, date.minute)
        super(Article, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('/%s/%s/%d' % (APP_LABEL, self.__class__.__name__, self.id)).lower()

    def get_next(self):
        try:
            return self.get_next_by_pub_date(visibility='visible')
        except ObjectDoesNotExist:
            return None

    def get_previous(self):
        try:
            return self.get_previous_by_pub_date(visibility='visible')
        except ObjectDoesNotExist:
            return None

    class Meta:
        abstract = True
        app_label = APP_LABEL
        ordering = ['-pub_date']


class Blog(Article):
    pass


class News(Article):
    pass
