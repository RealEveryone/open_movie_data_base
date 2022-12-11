from enum import Enum

from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify

from open_movie_data_base.user.validators import UsernameValidator, names_validator
from open_movie_data_base.utils.mixins import ChoicesMixin


class UserTypesChoices(ChoicesMixin, Enum):
    User = 'User'
    Actor = 'Actor'
    MovieDirector = 'Movie Director'


class AppUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UsernameValidator()

    username = models.CharField(
        max_length=35,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        }
    )

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "This email address is already in use by another user.",
        }
    )

    is_staff = models.BooleanField(
        default=False
    )
    is_regular_user = models.BooleanField(
        default=False)

    is_movie_director = models.BooleanField(
        default=False
    )
    is_actor = models.BooleanField(
        default=False
    )

    type_of_user = models.CharField(
        max_length=UserTypesChoices.get_length(),
        choices=UserTypesChoices.get_choices(),
        default='',
        blank=False
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ProfileMixin(models.Model):
    class Meta:
        abstract = True

    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MAX_LEN = 30

    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, primary_key=True
    )
    first_name = models.CharField(
        validators=[names_validator],
        max_length=FIRST_NAME_MAX_LEN,
        null=True, blank=True
    )
    last_name = models.CharField(
        validators=[names_validator],
        max_length=LAST_NAME_MAX_LEN,
        null=True, blank=True
    )
    birth_date = models.DateField(
        null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True
    )

    slug = models.SlugField(
        unique=True
    )

    profile_picture = CloudinaryField(
        null=True, blank=True
    )

    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return self.user.username
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class RegularUser(ProfileMixin):
    pass


class MovieCrew(ProfileMixin):
    class Meta:
        abstract = True

    filmography = models.TextField(
        null=True, blank=True
    )
    biography = models.TextField(
        null=True, blank=True
    )


class Actor(MovieCrew):
    pass


class MovieDirector(MovieCrew):
    pass
