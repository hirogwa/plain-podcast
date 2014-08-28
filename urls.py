from django.conf.urls import patterns, url
from feed import AllEpisodesFeed
import settings
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^episode/(?P<slug>\S+)/$', views.episode, name='episode'),
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),
    url(r'^{}(?P<path>.*)$'.format(settings.PRIVATE_FILE_URL.lstrip('/')),
        views.private_resources, name='private_resources')
)
