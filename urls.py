from django.conf.urls import patterns, url
from feed import AllEpisodesFeed
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^episode/(?P<slug>\S+)/$', views.episode, name='episode'),
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),
)
