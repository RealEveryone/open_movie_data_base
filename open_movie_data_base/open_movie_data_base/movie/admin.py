from django.contrib import admin

from open_movie_data_base.movie.models import Movie, MovieGenres


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display =['title', 'movie_director', 'uploaded_on']


@admin.register(MovieGenres)
class MovieGenresAdmin(admin.ModelAdmin):
    pass
