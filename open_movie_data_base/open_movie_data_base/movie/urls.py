from django.urls import path

from open_movie_data_base.movie.views import AddMovie, movie_details, Top100Movies, favourite_movies, MyMovies, \
    movie_edit, movie_reviews
from ..common.views import like_func, movie_reviews_likes, delete_movie_review

urlpatterns = [
    path('add/', AddMovie.as_view(), name='add-movie'),
    path('details/<slug:slug>/', movie_details, name='movie-details'),
    path('details/<slug:slug>/reviews/', movie_reviews, name='movie-reviews'),

    path('edit/<slug:slug>/', movie_edit, name='movie-edit'),
    path('top-100', Top100Movies.as_view(), name='top-100'),
    path('like/<pk>/', like_func, name='like-movie'),
    path('review/like/<pk>/', movie_reviews_likes, name='like-review'),
    path('review/delete/<pk>', delete_movie_review, name='delete-review'),
    path('favourite/', favourite_movies, name='favourite-movies'),
    path('my-movie/', MyMovies.as_view(), name='my-movies'),

]

from .signals import *
