from django.conf.urls import patterns, url
from plainpodcast.feed import AllEpisodesFeed
import plainpodcast.settings as settings
import plainpodcast.views as views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^feed/$', AllEpisodesFeed(), name='feed'),

    # articles
    url(r'^news/author/(?P<author>\S+)/$', views.news, name='news_by_author'),
    url(r'^news/(?P<article_id>\S+)/$', views.news, name='news'),
    url(r'^news/$', views.news, name='news'),

    url(r'^blog/author/(?P<author>\S+)/$', views.blog, name='blog_by_author'),
    url(r'^blog/(?P<article_id>\S+)/$', views.blog, name='blog'),
    url(r'^blog/$', views.blog, name='blog'),

    # episodes
    url(r'^episode/(?P<slug>\S+)/$', views.episode, name='episode'),
    url(r'^episodes/$', views.episodes, name='episodes'),
)
