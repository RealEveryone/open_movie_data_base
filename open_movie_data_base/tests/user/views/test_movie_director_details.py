from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from open_movie_data_base.common.models import Review
from open_movie_data_base.user.models import MovieDirector
from tests.base import CreateMovie

UserModel = get_user_model()


class TestMovieDirectorView(TestCase):

    def test_overall_rating__when_there_are_no_movies__expect_zero(self):
        movie_count = 0
        expected_result = 0
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        # CreateMovie(movie_director, movie_count)

        response = self.client.get(reverse('director-details', kwargs={'slug': movie_director.slug}))

        self.assertEqual(expected_result, response.context['overall_rating'])

    def test_overall_rating__when_there_are_movies__expect_result(self):
        MOVIE_COUNT = 2
        expected_result = 7.5
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        movies = CreateMovie(movie_director, MOVIE_COUNT)

        review1 = Review(user=user, movie=movies[0], rating=10, review='text')
        review1.save()

        response = self.client.get(reverse('director-details', kwargs={'slug': movie_director.slug}))
        # movies, get initialize with rating of zero ,
        # so when 10 is given as score for one out of two movies we have 10 + 0 / 2 = 5 so this is the expected outcome
        # for better understanding check common/views/AverageReviewScore and common/signals
        self.assertEqual(5, response.context['overall_rating'])

        review2 = Review(user=user, movie=movies[1], rating=5, review='text')
        review2.save()

        response = self.client.get(reverse('director-details', kwargs={'slug': movie_director.slug}))

        self.assertEqual(expected_result, response.context['overall_rating'])
