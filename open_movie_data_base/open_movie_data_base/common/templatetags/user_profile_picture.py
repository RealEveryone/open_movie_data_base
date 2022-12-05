from django.template import Library

from open_movie_data_base.utils.func import get_type_of_user

register = Library()


@register.filter
def profile_picture(user):
    user_type = get_type_of_user(user)
    return user_type.profile_picture


@register.filter
def profile_name(user):
    user_type = get_type_of_user(user)
    return user_type


@register.filter
def profile_slug(user):
    user_type = get_type_of_user(user)
    return user_type.slug

@register.filter
def profile_details_url(user):
    if user.is_movie_director:
        return 'director-details'
    elif user.is_actor:
        return 'actor-details'
    elif user.is_regular_user:
        return 'profile-details'
