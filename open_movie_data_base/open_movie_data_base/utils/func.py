def get_user_favourite_movies(request):
    user = request.user
    if user.is_authenticated:
        like_set = user.like_set.all()
        return [like.like_obj for like in like_set]


def get_type_of_user(user):
    if user.is_movie_director:
        return user.moviedirector
    elif user.is_actor:
        return user.actor
    elif user.is_regular_user:
        return user.regularuser
