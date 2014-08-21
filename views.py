from django.shortcuts import render, get_object_or_404
from models import Episode, Podcast, Statement, Presenter


def index(request):
    context = {'episodes': Episode.objects.all().order_by('-pub_date')}
    context.update(get_common_context(request))
    return render(request, 'podcast/index.html', context)


def about(request):
    presenters = Presenter.objects.all().order_by('display_order')
    context = {'presenters': presenters}
    context.update(get_common_context(request))
    return render(request, 'podcast/about.html', context)


def episode(request, slug):
    episode_obj = get_object_or_404(Episode, slug=slug)
    context = {'episode': episode_obj}
    context.update(get_common_context(request))
    return render(request, 'podcast/episode.html', context)


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
