from django.shortcuts import render, get_object_or_404
from models import Episode, Podcast


def index(request):
    episodes = Episode.objects.all().order_by('-pub_date')
    context = {'episodes': episodes}
    context.update(get_common_context())
    return render(request, 'podcast/index.html', context)


def episode(request, slug):
    episode = get_object_or_404(Episode, slug=slug)
    context = {'episode': episode}
    context.update(get_common_context())
    return render(request, 'podcast/episode.html', context)


def get_common_context():
    podcast = get_object_or_404(Podcast, pk=1)
    context = {'podcast': podcast}
    return context
