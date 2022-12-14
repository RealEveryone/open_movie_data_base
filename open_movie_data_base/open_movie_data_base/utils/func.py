def get_user_favourite_movies(request):
    user = request.user
    if user.is_authenticated:
        like_set = user.favouritemovies_set.all()
        return [like.like_obj for like in like_set]


def get_review_set_likes(request):
    user = request.user
    if user.is_authenticated:
        like_set = user.reviewlike_set.all()
        return [like.like_obj for like in like_set]


def get_general_like(request):
    user = request.user
    if user.is_authenticated:
        like_set = user.like_set.all()
        return [like.liked_movie for like in like_set]


def get_type_of_user(user):
    if user.is_movie_director:
        return user.moviedirector
    elif user.is_actor:
        return user.actor
    elif user.is_regular_user:
        return user.regularuser


def get_movie_objects(ll):
    return [actor for actor in ll]


def get_movie_reviews_ordered_by_likes(movie):
    return movie.review_set.all()


def is_movie_director_and_owner(user, movie):
    if user.is_movie_director:
        if user.moviedirector == movie.movie_director:
            return True
    return False


def user_is_owner_of_profile(request, user):
    return request.user == user.user


def return_user_review_if_exist(movie, user):
    if user.is_authenticated:
        for review in user.review_set.all():
            if review.movie == movie:
                return review
    return None
