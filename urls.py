from django.conf.urls import patterns, url
from feed import AllEpisodesFeed

urlpatterns = patterns('',
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),
)
