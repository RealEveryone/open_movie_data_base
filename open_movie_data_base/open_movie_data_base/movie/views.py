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
from open_movie_data_base.common.models import AverageReviewScore, Review
from open_movie_data_base.movie.forms import AddMovieForm, MovieEditForm
from open_movie_data_base.movie.mixins import MustBeMovieDirectorMixin
from open_movie_data_base.movie.models import Movie
from open_movie_data_base.utils.func import get_user_favourite_movies, get_review_set_likes

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
        context['is_banned'] = True
        return context
    # todo: find a way to save with signals ( you need to
    #  get current user
    #  in signal )
    #  You tried to save AverageReviewScore through signals but , circular saves from model and form_valid
    #  raised UNIQUE CONSTRAIN FAILED ERROR


class Top100Movies(generic.ListView):
    model = Movie
    template_name = 'movie/top-100-movies.html'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by('-averagereviewscore__score')[:100]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['user_favourite_movies'] = get_user_favourite_movies(request=self.request)
        context['is_banned'] = True
        return context


class MyMovies(LoginRequiredMixin, MustBeMovieDirectorMixin, generic.ListView):
    model = Movie
    template_name = 'movie/my_movies.html'
    paginate_by = 5

    def get_queryset(self):
        movie_director = self.request.user.moviedirector
        return super().get_queryset().filter(movie_director__exact=movie_director)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['is_banned'] = True
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

    if request.method == 'GET':
        form = ReviewForm()

    else:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()

    context = {
        'is_banned': True,
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
        'is_banned': True,
    }
    return render(request, 'favourite-movies.html', context)


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
        'is_banned': True,
        'user': user,
        'form': form,
        'edit': True
    }
    return render(request, 'movie/edit-movie.html', context=context)


def movie_reviews(request, slug):
    movie = Movie.objects.filter(slug=slug).get()
    reviews = movie.review_set.all()
    review_like_set = get_review_set_likes(request)

    order_by = request.GET.get('order_by')
    if order_by:
        if order_by == 'likes':
            reviews = reviews.annotate(likes=Count('reviewlike')).order_by('-likes', '-posted_on')
        else:
            reviews = reviews.order_by(order_by)

    context = {
        'movie': movie,
        'reviews': reviews,
        'is_banned': True,
        'user_liked_reviews': review_like_set
    }
    return render(request, 'movie_reviews.html', context)


def get_movie_objects(ll):
    return [actor for actor in ll]


def get_movie_reviews_ordered_by_likes(movie):
    return movie.review_set.all()


def is_movie_director_and_owner(user, movie):
    if user.is_movie_director:
        if user.moviedirector == movie.movie_director:
            return True
    return False
