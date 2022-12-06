from django.urls import path

from open_movie_data_base.common.views import *

urlpatterns = [
    path('home/', Index.as_view(), name='home-page'),
    path('redirect-to/', dispatcher, name='dispatcher'),
    path('add-to-favourite/<pk>/', add_to_favourite_movies, name='add-to-favourite'),
    path('like/<pk>/', general_movie_like, name='like-movie'),
    path('review/like/<pk>/', movie_reviews_likes, name='like-review'),
    path('review/delete/<pk>', delete_movie_review, name='delete-review'),
    path('details/<slug:slug>/reviews/', movie_reviews, name='movie-reviews'),

]

from .signals import *
