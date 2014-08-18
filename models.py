from django.db import models
import mimetypes


class Podcast(models.Model):
    name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    domain = models.URLField()
    itunes_url = models.URLField(blank=True)
    facebook_page = models.URLField(blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)
    facebook_app_id = models.CharField(max_length=30, blank=True)

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

