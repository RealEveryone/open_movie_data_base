from django.urls import path

from open_movie_data_base.movie.views import AddMovie, movie_details, Top100Movies, favourite_movies, MyMovies, \
    movie_edit, DeleteMovie

urlpatterns = [
    path('add/', AddMovie.as_view(), name='add-movie'),
    path('details/<slug:slug>/', movie_details, name='movie-details'),
    path('edit/<slug:slug>/', movie_edit, name='movie-edit'),
    path('delete/<pk>/', DeleteMovie.as_view(), name='delete-movie'),
    path('top-100', Top100Movies.as_view(), name='top-100'),
    path('favourite/', favourite_movies, name='favourite-movies'),
    path('my-movie/', MyMovies.as_view(), name='my-movies'),

]

from .signals import *
