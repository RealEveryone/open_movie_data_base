from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.cache import cache_page

from open_movie_data_base.common.forms import ReviewForm
from open_movie_data_base.movie.forms import AddMovieForm, MovieEditForm
from open_movie_data_base.movie.mixins import MustBeMovieDirectorMixin
from open_movie_data_base.movie.models import Movie
from open_movie_data_base.utils.func import get_user_favourite_movies, \
    is_movie_director_and_owner, get_movie_objects, get_general_like

UserModel = get_user_model()


class AddMovie(LoginRequiredMixin, MustBeMovieDirectorMixin, generic.CreateView):
    form_class = AddMovieForm
    template_name = 'movie/add-movie.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        movie = form.save(commit=False)
        movie_director = self.request.user.moviedirector
        movie.movie_director = movie_director
        movie.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Top100Movies(generic.ListView):
    model = Movie
    template_name = 'movie/top-100-movies.html'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by('-averagereviewscore__score')[:100]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['user_favourite_movies'] = get_user_favourite_movies(request=self.request)
        context['user_liked_movies'] = get_general_like(self.request)

        return context
    # todo: Make AdditionalContentMixin for user_favourite_movies/user_liked_movies


class MyMovies(LoginRequiredMixin, MustBeMovieDirectorMixin, generic.ListView):
    model = Movie
    template_name = 'movie/my_movies.html'
    paginate_by = 5

    def get_queryset(self):
        movie_director = self.request.user.moviedirector
        return super().get_queryset().filter(movie_director__exact=movie_director)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['user_favourite_movies'] = get_user_favourite_movies(self.request)
        return context


# @cache_page(60 * 1)
def movie_details(request, slug):
    try:
        movie = Movie.objects. \
            filter(slug=slug). \
            get()

    except Movie.DoesNotExist:
        raise Http404

    form = ReviewForm()

    # relocate to different view
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('sign-in')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie-reviews', movie.slug)

    context = {
        'object': movie,
        'actors': get_movie_objects(movie.actors.all()),
        'genres': get_movie_objects(movie.genres.all()),
        'average_rating': movie.averagereviewscore.score,
        'reviews': movie.review_set.annotate(likes=Count('reviewlike')).order_by('-likes', 'posted_on')[:3],
        'form': form
    }

    return render(request, 'movie/movie-details.html', context)


def favourite_movies(request):
    if not request.user.is_authenticated:
        return redirect('sign-in')

    user_favourite_movies = get_user_favourite_movies(request=request)
    paginator = Paginator(user_favourite_movies, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'user_liked_movies': get_general_like(request)

    }
    return render(request, 'movie/favourite-movies.html', context)


def movie_edit(request, slug):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    movie = Movie.objects.filter(slug=slug).get()
    user = request.user
    if not is_movie_director_and_owner(user, movie):
        return render(request, 'must-be-movie-director.html')

    if request.method == 'POST':
        form = MovieEditForm(request.POST, request.FILES, instance=movie)

    else:
        form = MovieEditForm(instance=movie)

    context = {
        'user': user,
        'form': form,
        'edit': True
    }
    return render(request, 'movie/edit-movie.html', context=context)


def delete_movie(request, pk):
    movie = Movie.objects.filter(pk=pk).get()
    if not is_movie_director_and_owner(request.user, movie):
        return render(request, 'must-be-movie-director.html')

    if request.method == 'POST':
        movie.delete()
        return redirect('my-movies')

    context = {
        'object': movie
    }

    return render(request, 'movie/delete_movie.html', context)
