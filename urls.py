from django.conf.urls import patterns, url
from feed import AllEpisodesFeed
import settings
import views

urlpatterns = patterns('',
    # with no parameter
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^episodes/$', views.episodes, name='episodes'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),

    # with parameter
    url(r'^episode/(?P<slug>\S+)/$', views.episode, name='episode'),

    # private views
    url(r'^private/preview/$', views.scheduled_list, name='scheduled_list'),
    url(r'^private/preview/episode/(?P<slug>\S+)/$', views.scheduled_episode, name='scheduled_episode'),
    url(r'^{}(?P<path>.*)$'.format(settings.PRIVATE_FILE_URL.lstrip('/')),
        views.private_resources, name='private_resources')
)
