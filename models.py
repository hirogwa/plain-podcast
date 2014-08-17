from django.db import models


class Podcast(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    domain = models.URLField()
    # itunes_url = models.URLField()
    facebook_app_id = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return self.name


class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    show_notes = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='episode', blank=True)
    pub_date = models.DateTimeField('published_time')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/podcast/episode/%d' % self.id
