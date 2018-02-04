from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import Webtoon


def webtoon_list(request):
    webtoon = get_list_or_404(Webtoon)
    context = {
        'webtoon_list': webtoon,
    }
    return render(request, 'webtoon/webtoon_list.html', context)


def webtoon_detail(request, webtoon_pk):
    webtoon = get_object_or_404(Webtoon, pk=webtoon_pk)
    webtoon.get_episode_list()
    context = {
        'webtoon': webtoon,
    }
    return render(request, 'webtoon/webtoon_detail.html', context)