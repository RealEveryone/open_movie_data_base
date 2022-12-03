def get_user_favourite_movies(request):
    user = request.user
    if user.is_authenticated:
        like_set = user.like_set.all()
        return [like.like_obj for like in like_set]