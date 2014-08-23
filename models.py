from django.db import models
import mimetypes


class Podcast(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    media_url = models.URLField()
    app_root_url = models.URLField()
    logo_horizontal = models.ImageField(upload_to='images')
    itunes_url = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    twitter_hashtag = models.CharField(max_length=100, blank=True)
    twitter_timeline_widget_id = models.CharField(max_length=30, blank=True)
    facebook_app_id = models.CharField(max_length=30, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


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

    def get_mime_type(self):
        return mimetypes.guess_type(self.audio_file.name)[0]

    def get_absolute_url(self):
        return '/podcast/episode/%s' % self.slug


class Presenter(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    thumbnail_square = models.ImageField(upload_to='images')
    display_order = models.IntegerField(blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    facebook_page = models.URLField(blank=True)
    personal_site = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.display_order is None:
            self.display_order = 100
        super(Presenter, self).save(*args, **kwargs)


class Statement(models.Model):
    unique_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    statement = models.TextField()

    def __unicode__(self):
        return self.unique_name
