from django.contrib.auth import get_user_model
from django.urls import reverse

from open_movie_data_base.common.models import Like, Review
from open_movie_data_base.user.models import MovieDirector
from tests.base import BaseTestCase, CreateMovie, create_genre

UserModel = get_user_model()


class TestHomePageView(BaseTestCase):

    def test_home_page__when_there_are_no_movie__expect_none(self):
        response = self.client.get(reverse('home-page'))

        self.assertCollectionEmpty(response.context['object_list'])

    def test_home_page__when_there_are_movies__expect_movies(self):
        movie_count = 5
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        CreateMovie(movie_director, movie_count)

        response = self.client.get(reverse('home-page'))

        self.assertEqual(movie_count, len(response.context['object_list']))

    def test_home_page__when_ordering_movies_by_genre__if_movie_in_stated_genre_expect_movie(self):
        MOVIE_COUNT = 1
        stated_genre = 'Action'
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        movies = CreateMovie(movie_director, MOVIE_COUNT)
        stated_movie_genre = create_genre(stated_genre)
        movies[0].genres.add(stated_movie_genre)

        response = self.client.get(reverse('home-page'), data={'genres': stated_movie_genre.pk})

        self.assertEqual(1, len(response.context['object_list']))

    def test_home_page__when_ordering_movies_by_genre__if_movie_not_in_stated_genre_expect_no_movie(self):
        MOVIE_COUNT = 1
        genre = 'Action'
        stated_movie_genre = 'Horror'
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        movies = CreateMovie(movie_director, MOVIE_COUNT)
        movie_genre = create_genre(genre)
        movies[0].genres.add(movie_genre)

        stated_movie_genre = create_genre(stated_movie_genre)

        response = self.client.get(reverse('home-page'), data={'genres': stated_movie_genre.pk})

        self.assertEqual(0, len(response.context['object_list']))

    def test_home_page__when_paginated__expect_5_movies_of_each_page(self):
        MOVIE_COUNT = 10
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        CreateMovie(movie_director, MOVIE_COUNT)

        response = self.client.get(reverse('home-page'), data={'page': 1})

        self.assertEqual(5, len(response.context['object_list']))

        response = self.client.get(reverse('home-page'), data={'page': 2})

        self.assertEqual(5, len(response.context['object_list']))

    def test_home_page__when_paginated__but_page_is_out_of_index__404_not_found(self):
        MOVIE_COUNT = 5
        status_code = 404
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        CreateMovie(movie_director, MOVIE_COUNT)

        response = self.client.get(reverse('home-page'), data={'page': 2})
        self.assertEqual(status_code, response.status_code)

    def test_home_page__ordering_by_like__expect_movie_collection_ordered_by_likes(self):
        MOVIE_COUNT = 5
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        movies = CreateMovie(movie_director, MOVIE_COUNT)
        marked_movie = movies[0]

        response = self.client.get(reverse('home-page'))

        self.assertNotEqual(marked_movie, response.context['object_list'][0])

        like = Like(user=user, liked_movie=marked_movie)
        like.save()

        response = self.client.get(reverse('home-page'), data={'filters': 'likes'})

        self.assertEqual(marked_movie, response.context['object_list'][0])

    def test_home_page__ordering_by_rating__expect_movie_collection_ordered_by_rating(self):
        MOVIE_COUNT = 5
        user = UserModel.objects.create(
            username='username', password='Os02k#aKP002', email='email@email.com', type_of_user='MovieDirector'
        )
        movie_director = MovieDirector(
            user=user
        )
        movie_director.save()

        movies = CreateMovie(movie_director, MOVIE_COUNT)
        marked_movie = movies[0]

        response = self.client.get(reverse('home-page'))

        self.assertNotEqual(marked_movie, response.context['object_list'][0])

        review = Review(user=user, movie=marked_movie, rating=10.00, review='description')
        review.save()

        response = self.client.get(reverse('home-page'), data={'filters': 'rating'})

        self.assertEqual(marked_movie, response.context['object_list'][0])
