from django.shortcuts import render


class MustBeMovieDirectorMixin:
    def get(self, *args, **kwargs):
        if not self.request.user.is_movie_director:
            return render(self.request, 'must-be-movie-director.html')
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_movie_director:
            return render(self.request, 'must-be-movie-director.html')
        return super().post(*args, **kwargs)
