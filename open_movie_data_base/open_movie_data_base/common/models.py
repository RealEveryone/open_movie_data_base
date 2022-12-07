from django.contrib.auth import get_user_model
from django.db import models

from open_movie_data_base.common.validators import InRangeValidator
from open_movie_data_base.movie.models import Movie

UserModel = get_user_model()


class Review(models.Model):
    MIN_RATING_NUM = 0.00
    MAX_RATING_NUM = 10.00
    ERR_MSG = f'Value must be between {MIN_RATING_NUM} and {MAX_RATING_NUM}'
    REVIEW_MAX_LEN = 600
    review = models.CharField(
        max_length=REVIEW_MAX_LEN
    )
    rating = models.FloatField(
        validators=[InRangeValidator(0.00, 10.00, ERR_MSG)]
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    posted_on = models.DateField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return self.movie.title


class AverageReviewScore(models.Model):
    movie = models.OneToOneField(
        Movie, on_delete=models.CASCADE
    )
    total_sum_of_numbers = models.FloatField(
    )
    score = models.FloatField(
        default=0
    )


class FavouriteMovies(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    like_obj = models.ForeignKey(
        Movie, on_delete=models.CASCADE
    )


class Like(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    liked_movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE
    )


class ReviewLike(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE
    )
    like_obj = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )
