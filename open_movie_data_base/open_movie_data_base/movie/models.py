from enum import Enum

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from open_movie_data_base.movie.validators import validate_file_size
from open_movie_data_base.user.models import Actor, MovieDirector
from open_movie_data_base.utils.mixins import ChoicesMixin
from open_movie_data_base.utils.validators import CharValidator

from cloudinary.models import CloudinaryField


class MovieGenresChoices(ChoicesMixin, Enum):
    action = 'Action'
    adventure = 'Adventure'
    comedy = 'Comedy'
    drama = 'Drama'
    fantasy = 'Fantasy'
    horror = 'Horror'
    musicals = 'Musicals'
    mystery = 'Mystery'
    romance = 'Romance'
    science = 'Science'
    fiction = 'Fiction'
    sports = 'Sports'
    thriller = 'Thriller'
    Western = 'Western'

    # Use this for reference about the category when cleaning DB


class MovieGenres(models.Model):
    CATEGORY_MAX_LEN = 50
    REGEX_PATTERN = r"^[A-Za-z\w-]+\Z"
    ERR_MSG = 'Use only latin letters, spaces and dashes'
    category = models.CharField(
        max_length=CATEGORY_MAX_LEN,
        validators=[CharValidator(REGEX_PATTERN, ERR_MSG)],
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'MovieGenres'

    def __str__(self):
        return self.category


class Movie(models.Model):
    MOVIE_TITLE_MAX_LEN = 50
    MOVIE_TITLE_REGEX_PATTERN = r"^[\s\w.-]+\Z"
    MOVIE_TITLE_ERROR_MSG = "Movie title may contain only latin letters, numbers, and dashes between characters."
    MOVIE_TITLE_VALIDATOR = CharValidator(MOVIE_TITLE_REGEX_PATTERN, MOVIE_TITLE_ERROR_MSG)

    MOVIE_DESCRIPTION_MIN_LEN = 300
    MOVIE_DESCRIPTION_MAX_LEN = 1200

    movie_director = models.ForeignKey(
        MovieDirector, on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=MOVIE_TITLE_MAX_LEN,
        validators=[MOVIE_TITLE_VALIDATOR]
    )

    release_date = models.DateField(
    )

    age_restriction = models.PositiveIntegerField(
    )

    description = models.CharField(
        validators=[MinLengthValidator(MOVIE_DESCRIPTION_MIN_LEN)],
        max_length=MOVIE_DESCRIPTION_MAX_LEN,
        help_text='The first 40 characters will be displayed as short description',
        error_messages={
            "min_length": 'Movie description must be at least 300 characters',
            'max_length': 'Movie description can only be 1200 characters'
        }

    )
    # todo: add validator for description

    movie_poster = CloudinaryField(
        validators=[validate_file_size]
    )

    genres = models.ManyToManyField(
        MovieGenres, blank=True
    )

    actors = models.ManyToManyField(
        Actor, blank=True
    )

    movie_length = models.PositiveIntegerField(
        help_text='in minutes'
    )

    uploaded_on = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f'{self.title}-{self.pk}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Meta:
    ordering = ['-uploaded_on']
