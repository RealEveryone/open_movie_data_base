import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from open_movie_data_base.movie.models import Movie, MovieGenres
from open_movie_data_base.user.models import MovieDirector, Actor, RegularUser
from tests.utils import test_movie_description

UserModel = get_user_model()


def create_genre(genre):
    genre = MovieGenres(
        category=genre
    )
    genre.save()
    return genre


def CreateMovie(movie_director, movie_count):
    collection = [Movie(movie_director=movie_director,
                        title=f'{x}',
                        release_date=datetime.date.today(),
                        age_restriction=21,
                        description=test_movie_description,
                        movie_poster='pic.jpg', movie_length=150,
                        )
                  for x in range(movie_count)]
    [x.save() for x in collection]
    return collection


class BaseTestCase(TestCase):

    def assertCollectionEmpty(self, collection):
        return self.assertEqual(0, len(collection))
