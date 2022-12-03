from django.shortcuts import redirect
from django.views import generic as views
from django.views.generic.list import BaseListView


class IsMovieDirectorMixin:

    def get(self, *args, **kwargs):
        if not self.request.user.is_movie_director:
            return redirect('home-page')
        return super().get(*args, **kwargs)

    try:
        def post(self, *args, **kwargs):
            if not self.request.user.is_movie_director:
                return redirect('home-page')
            return super().post(*args, **kwargs)
    except:
        pass
