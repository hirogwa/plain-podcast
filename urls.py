from django.conf.urls import patterns, url
from feed import AllEpisodesFeed
import settings
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^episode/(?P<slug>\S+)/$', views.episode, name='episode'),

    url(r'^private/preview/$', views.scheduled_list, name='scheduled_list'),
    url(r'^private/preview/episode/(?P<slug>\S+)/$', views.scheduled_episode, name='scheduled_episode'),

    url(r'^about/$', views.about, name='about'),
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),
    url(r'^{}(?P<path>.*)$'.format(settings.PRIVATE_FILE_URL.lstrip('/')),
        views.private_resources, name='private_resources')
)
