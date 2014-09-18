from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since
from models import *
import mimetypes
import os.path
import settings
import stat

ARTICLE_LIST_SIZE = 5
PAGE_CTRL_SIZE = 2


def index(request):
    episodes_all = Episode.objects.all().order_by('-pub_date')
    news_all = News.objects.filter(visibility='visible').order_by('-pub_date')
    blog_all = Blog.objects.filter(visibility='visible').order_by('-pub_date')
    context = {'episodes': episodes_all,
               'episodes_recent': episodes_all[:9],
               'news_recent': news_all[:5],
               'blog_recent': blog_all[:5],
               'promotions': Promotion.objects.filter(active='active').order_by('display_order', '-update_datetime'),
               }
    context.update(get_common_context(request))
    return render(request, template_file(context, 'index'), context)


def article(request, base_articles, template, article_id):
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
    next_item = None
    prev_item = None
    try:
        next_item = target_article.get_next_by_pub_date
        prev_item = target_article.get_previous_by_pub_date
    except ObjectDoesNotExist:
        pass
    context['next_item'] = next_item
    context['prev_item'] = prev_item

    # other needs
    context.update({'all_articles': base_articles.order_by('-pub_date'),
                    'authors': get_article_author_map(base_articles),
                    })
    context.update(get_common_context(request))
    return render(request, template_file(context, template), context)


def get_article_author_map(base_articles):
    """
    given list of articles, returns the dictionary of authors to their article counts
    :param base_articles:
    :return:
    """
    authors = {}
    for map_list in base_articles.values('author').annotate(author_count=Count('author')):
        author = Presenter.objects.filter(id=map_list['author'])
        if author:
            authors[author[0]] = map_list['author_count']
    return authors


def article_list(request, base_articles, template, presenter=None):
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
                    'authors': get_article_author_map(sorted_articles),
                    'preceding_pages': preceding_pages,
                    'succeeding_pages': succeeding_pages})
    context.update(get_common_context(request))
    return render(request, template_file(context, template), context)


def news(request, article_id=None, author=None):
    news_articles = News.objects.filter(visibility='visible')
    if article_id:
        return article(request, news_articles, 'news', article_id)
    else:
        return article_list(request, news_articles, 'news_list', presenter=author)


def blog(request, article_id=None, author=None):
    blog_articles = Blog.objects.filter(visibility='visible')
    if article_id:
        return article(request, blog_articles, 'blog', article_id)
    else:
        return article_list(request, blog_articles, 'blog_list', presenter=author)


def about(request):
    # main contents
    presenters = Presenter.objects.filter(visibility='visible').order_by('display_order')
    # for side bar
    news_articles = News.objects.filter(visibility='visible').order_by('-pub_date')
    blog_articles = Blog.objects.filter(visibility='visible').order_by('-pub_date')
    context = {'presenters': presenters,
               'news_articles': news_articles,
               'blog_articles': blog_articles}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'about'), context)


def episode(request, slug):
    episode_obj = get_object_or_404(Episode, slug=slug)
    context = {'episode': episode_obj}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'episode'), context)


def episodes(request):
    """
    :param request:
    :return: the list of episodes
    """
    context = {'episodes': Episode.objects.all().order_by('-pub_date')}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'episodes'), context)


def contact(request):
    context = {}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'contact'), context)


def scheduled_list(request):
    if request.user.is_authenticated():
        context = {'episodes': ScheduledEpisode.objects.all().order_by('-pub_date')}
        context.update(get_common_context(request))
        context.update(get_private_context(request))
        return render(request, 'podcast/scheduled_list.html', context)
    else:
        raise Http404()


def scheduled_episode(request, slug):
    if request.user.is_authenticated():
        episode_obj = get_object_or_404(ScheduledEpisode, slug=slug)
        context = {'episode': episode_obj}
        context.update(get_common_context(request))
        context.update(get_private_context(request))
        return render(request, 'podcast/scheduled_episode.html', context)
    else:
        raise Http404()


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


def get_private_context(request):
    return {'private_media_prefix': settings.PRIVATE_FILE_URL}


def template_file(context, template):
    return 'podcast/{}/{}.html'.format(context.get('podcast').theme, template)


def private_resources(request, path):
    if request.user.is_authenticated():
        full_path = os.path.join(settings.PRIVATE_FILE_ROOT, path)
        if not os.path.exists(full_path):
            raise Http404('resource not found:"{}"'.format(full_path))

        stat_obj = os.stat(full_path)
        mime_type = mimetypes.guess_type(full_path)[0]

        if not was_modified_since(
                request.META.get('HTTP_IF_MODIFIED_SINCE'),
                stat_obj[stat.ST_MTIME],
                stat_obj[stat.ST_SIZE]):
            return HttpResponseNotModified(content_type=mime_type)

        response = HttpResponse(open(full_path, 'rb').read(), content_type=mime_type)
        response["Last-Modified"] = http_date(stat_obj[stat.ST_MTIME])
        return response

    else:
        raise Http404()
