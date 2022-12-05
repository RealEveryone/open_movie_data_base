from django.contrib.auth import get_user_model, login
from django.db.models import signals
from django.dispatch import receiver

from open_movie_data_base.user.models import Actor, MovieDirector, RegularUser

UserModel = get_user_model()


@receiver(signals.pre_save, sender=UserModel)
def create_profile_type_on_user_creation(instance, *args, **kwargs):
    type_of_user = instance.type_of_user

    if type_of_user == 'Actor':
        instance.is_actor = True
    elif type_of_user == 'MovieDirector':
        instance.is_movie_director = True
        instance.is_staff = True
    elif type_of_user == 'User':
        instance.is_regular_user = True


@receiver(signals.post_save, sender=UserModel)
def create_profile_type_on_user_creation(instance, *args, **kwargs):
    type_of_user = instance

    if type_of_user.is_actor:
        Actor(
            user=instance,
        ).save()

    elif type_of_user.is_movie_director:
        MovieDirector(
            user=instance,
        ).save()

    elif type_of_user.is_regular_user:
        RegularUser(
            user=instance
        ).save()
