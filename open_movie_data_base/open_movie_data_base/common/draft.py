from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

from open_movie_data_base.movie.models import Movie
from open_movie_data_base.utils.func import get_user_favourite_movies


def home_page(request):
    object_list = Movie.objects.all()

    genre = request.GET.get('genre')
    if genre and genre != 'all':
        object_list = object_list.filter(genres__category__exact=genre)
    search_text = request.GET.get('searchbar')
    order_by = request.GET.get('filters')

    if order_by:

        if order_by in ['likes']:
            object_list = object_list.annotate(likes=Count('like')).order_by('likes')

        elif order_by in ['rating']:
            object_list = object_list.order_by('-averagereviewscore__score')

        else:
            object_list = object_list.order_by(order_by)

    if search_text:
        object_list = object_list.filter(title__icontains=search_text)

    paginator = Paginator(object_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_favourite_movies': get_user_favourite_movies(request=request),
        'page_obj': page_obj,

    }
    return render(request, 'index.html', context)
