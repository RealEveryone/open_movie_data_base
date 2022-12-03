from django.contrib.auth.views import LogoutView
from django.urls import path, include

from open_movie_data_base.user.views import SignUp, SignIn, ProfileDetails, ActorProfileDetails, MovieDirectorDetails, \
    edit_profile, edit_movie_director, edit_actor, profile_dispatcher

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),

    path('details/', include(
        [path('<slug:slug>/', ProfileDetails.as_view(), name='profile-details'),
         path('actors/<slug:slug>/', ActorProfileDetails.as_view(), name='actor-details'),
         path('movie-director/<slug:slug>/', MovieDirectorDetails.as_view(), name='director-details')]
    )),
    path('edit/', include(
        [path('<slug:slug>/', edit_profile, name='edit-profile'),
         path('movie-director/<slug:slug>/', edit_movie_director, name='edit-movie-director'),
         path('actor/<slug:slug>/', edit_actor, name='edit-actor')
         ]
    )),
    path('redirect-to-myprofile', profile_dispatcher, name='profile-dispatcher')
]

from .signals import *
