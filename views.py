from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since
from plainpodcast.models import *
import mimetypes
import os.path
import plainpodcast.settings as settings
import stat

ARTICLE_LIST_SIZE = 5
PAGE_CTRL_SIZE = 2


def theme_view():
    theme = Podcast.objects.all()[0].theme
    return THEMES[theme.name]


def index(request):
    return theme_view().index(request)


def about(request):
    return theme_view().about(request)


def contact(request):
    return theme_view().contact(request)


def news(request, **kwargs):
    return theme_view().news(request, **kwargs)


def blog(request, **kwargs):
    return theme_view().blog(request, **kwargs)


def episode(request, slug):
    return theme_view().episode(request, slug)


def episodes(request):
    return theme_view().episodes(request)


def scheduled_episode(request, slug):
    return theme_view().scheduled_episode(request, slug)


class View:
    def __init__(self):
        pass

    @staticmethod
    def get_common_context(request):
        podcast_obj = get_object_or_404(Podcast, pk=1)
        footer_about = Statement.objects.filter(unique_name='footer-about').first()
        footer_twitter = Statement.objects.filter(unique_name='footer-twitter').first()
        footer_subscription = Statement.objects.filter(unique_name='footer-subscription').first()
        context = {'host': request.META['HTTP_HOST'],
                   'podcast': podcast_obj,
                   'footer_about': footer_about,
                   'footer_twitter': footer_twitter,
                   'footer_subscription': footer_subscription,
                   }
        return context

    @classmethod
    def index(cls, request):
        context, template = cls.index_context(request)
        return render(request, template, context)

    @classmethod
    def index_context(cls, request):
        episodes_all = Episode.objects.all().order_by('-pub_date')

        context = {
            'episodes': episodes_all,
            'string_archived': cls._custom_string(
                'string-episode-archived', 'archived')
        }
        context.update(cls.get_common_context(request))
        return context, cls._template_file('index')

    @classmethod
    def about(cls, request):
        context, template = cls.about_context(request)
        return render(request, template, context)

    @classmethod
    def about_context(cls, request):
        presenters = Presenter.objects.filter(visibility='visible').order_by('display_order')
        context = {'presenters': presenters}
        context.update(cls.get_common_context(request))
        return context, cls._template_file('about')

    @classmethod
    def contact(cls, request):
        context, template = cls.contact_context(request)
        return render(request, template, context)

    @classmethod
    def contact_context(cls, request):
        context = cls.get_common_context(request)
        return context, cls._template_file('contact')

    @classmethod
    def news(cls, request, **kwargs):
        news_articles = News.objects.filter(visibility='visible')
        if 'article_id' in kwargs:
            return cls._article(request, news_articles, 'news', kwargs.get('article_id'))
        else:
            return cls._article_list(request, news_articles, 'news_list', presenter=kwargs.get('author'))

    @classmethod
    def blog(cls, request, **kwargs):
        blog_articles = Blog.objects.filter(visibility='visible')
        if 'article_id' in kwargs:
            return cls._article(request, blog_articles, 'blog', kwargs.get('article_id'))
        else:
            return cls._article_list(request, blog_articles, 'blog_list', presenter=kwargs.get('author'))

    @classmethod
    def episode(cls, request, slug):
        episode_obj = get_object_or_404(Episode, slug=slug)
        if episode_obj.pub_status == 'archived':
            raise Http404()

        context = {'episode': episode_obj}
        context.update(cls.get_common_context(request))
        return render(request, cls._template_file('episode'), context)

    @classmethod
    def episodes(cls, request):
        """
        :param request:
        :return: the list of episodes
        """
        context = {
            'episodes': Episode.objects.all().order_by('-pub_date'),
            'string_archived': cls._custom_string(
                'string-episode-archived', 'archived')
        }
        context.update(cls.get_common_context(request))
        return render(request, cls._template_file('episodes'), context)

    @classmethod
    def scheduled_episode(cls, request, slug):
        if request.user.is_authenticated():
            episode_obj = get_object_or_404(ScheduledEpisode, slug=slug)
            context = {'episode': episode_obj}
            context.update(cls.get_common_context(request))
            context.update(cls.get_private_context())
            return render(request, 'plainpodcast/scheduled_episode.html', context)
        else:
            raise Http404()


    @classmethod
    def get_common_context(cls, request):
        podcast_obj = get_object_or_404(Podcast, pk=1)
        footer_about = Statement.objects.filter(unique_name='footer-about').first()
        footer_twitter = Statement.objects.filter(unique_name='footer-twitter').first()
        footer_subscription = Statement.objects.filter(unique_name='footer-subscription').first()
        context = {'host': request.META['HTTP_HOST'],
                   'podcast': podcast_obj,
                   'footer_about': footer_about,
                   'footer_twitter': footer_twitter,
                   'footer_subscription': footer_subscription,
                   }
        return context

    @staticmethod
    def get_private_context():
        return {'private_media_prefix': settings.PRIVATE_FILE_URL}

    @classmethod
    def _get_article_author_map(cls, article_class_name):
        """
        given list of articles, returns the dictionary of authors to their article counts
        :param base_articles:
        :return:
        """
        filter_kwarg = {article_class_name.lower() + '__visibility': 'visible'}
        author_counts = Presenter.objects \
            .filter(**filter_kwarg) \
            .annotate(article_count=Count(article_class_name.lower()))

        authors = {}
        for author in author_counts:
            authors[author] = author.article_count
        return authors

    @classmethod
    def _article(cls, request, base_articles, template, article_id):
        """
        renders the page for single article
        :param request:
        :param base_articles:
        :param template:
        :param article_id:
        :return:
        """
        context = {}

        # target article
        target_article_candidate = base_articles.filter(id=article_id)
        if not target_article_candidate:
            raise Http404
        target_article = target_article_candidate[0]
        context['articles'] = [target_article]

        # previous and next article
        context['next_item'] = target_article.get_next
        context['prev_item'] = target_article.get_previous

        # other needs
        context.update({'all_articles': base_articles.order_by('-pub_date'),
                        'authors': cls._get_article_author_map(base_articles.model.__name__),
                        })
        context.update(cls.get_common_context(request))
        return render(request, cls._template_file(template), context)

    @classmethod
    def _article_list(cls, request, base_articles, template, presenter=None):
        """
        renders the page for article list
        :param request:
        :param base_articles:
        :param template:
        :param presenter:
        :param article_id:
        :return:
        """
        context = {}

        # sort
        sorted_articles = base_articles.order_by('-pub_date')

        # filter
        filters = {}
        filtered_articles = sorted_articles
        if presenter:
            filters['author'] = Presenter.objects.get(id=presenter)
            filtered_articles = filtered_articles.filter(author=presenter)

        # prepare paginated article list
        paginator = Paginator(filtered_articles, ARTICLE_LIST_SIZE)
        page_number = request.GET.get('page')
        try:
            articles = paginator.page(page_number)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        # page control info
        preceding_pages = []
        for x in range(1, articles.number):
            if len(preceding_pages) == PAGE_CTRL_SIZE:
                break
            preceding_pages.insert(0, articles.number - x)
        succeeding_pages = []
        for x in range(articles.number + 1, paginator.num_pages + 1):
            if len(succeeding_pages) == PAGE_CTRL_SIZE:
                break
            succeeding_pages.append(x)

        # returned values
        context.update({'articles': articles,
                        'all_articles': sorted_articles,
                        'filters': filters,
                        'authors': cls._get_article_author_map(base_articles.model.__name__),
                        'preceding_pages': preceding_pages,
                        'succeeding_pages': succeeding_pages})
        context.update(cls.get_common_context(request))
        return render(request, cls._template_file(template), context)

    @staticmethod
    def _template_file(template):
        theme = Podcast.objects.all()[0].theme
        return 'plainpodcast/{}/{}.html'.format(theme.name, template)

    @staticmethod
    def _custom_string(unique_name, default_string=''):
        custom_string_obj = CustomString.objects.filter(
            unique_name=unique_name).first()
        if custom_string_obj:
            return custom_string_obj.custom_string
        else:
            return default_string


class Wide(View):
    @classmethod
    def index_context(cls, request):
        context, template = View.index_context(request)
        news_all = News.objects.filter(visibility='visible').order_by('-pub_date')
        blog_all = Blog.objects.filter(visibility='visible').order_by('-pub_date')
        context.update({'episodes_recent': context['episodes'][:9],
                        'news_recent': news_all[:5],
                        'blog_recent': blog_all[:5],
                        'promotions': Promotion.objects.filter(
                            active='active').order_by('display_order', '-update_datetime'),
                        })
        return context, template

    @classmethod
    def about_context(cls, request):
        context, template = View.about_context(request)
        news_articles = News.objects.filter(visibility='visible').order_by('-pub_date')
        blog_articles = Blog.objects.filter(visibility='visible').order_by('-pub_date')
        context.update({'news_articles': news_articles,
                        'blog_articles': blog_articles})
        return context, template


class Plain(View):
    @classmethod
    def contact_context(cls, request):
        raise Http404

    @classmethod
    def news(cls, request, **kwargs):
        raise Http404

    @classmethod
    def blog(cls, request, **kwargs):
        raise Http404


THEMES = {'plain-yogurt': Plain(),
          'wide': Wide()}
