from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
from django.views.static import was_modified_since
from models import Episode, Podcast, Statement, Presenter, ScheduledEpisode, Promotion
import mimetypes
import os.path
import settings
import stat


def index(request):
    episodes = Episode.objects.all().order_by('-pub_date')
    context = {'episodes': episodes,
               'recent_episodes': episodes[:5],
               'promotions': Promotion.objects.filter(active='active').order_by('display_order', '-update_datetime'),
               }
    context.update(get_common_context(request))
    return render(request, template_file(context, 'index'), context)


def news(request):
    context = {'episodes': Episode.objects.all().order_by('-pub_date')}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'news'), context)


def about(request):
    presenters = Presenter.objects.filter(visibility='visible').order_by('display_order')
    context = {'presenters': presenters}
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


def blog(request):
    context = {'episodes': Episode.objects.all().order_by('-pub_date')}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'episodes'), context)


def contact(request):
    context = {'episodes': Episode.objects.all().order_by('-pub_date')}
    context.update(get_common_context(request))
    return render(request, template_file(context, 'episodes'), context)


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
