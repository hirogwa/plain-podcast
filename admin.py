from django.contrib import admin
from models import Podcast, Episode, Presenter, Statement, ScheduledEpisode, ITunesInfo

# Register your models here.
admin.site.register(Podcast)
admin.site.register(Episode)
admin.site.register(Presenter)
admin.site.register(Statement)
admin.site.register(ScheduledEpisode)
admin.site.register(ITunesInfo)
