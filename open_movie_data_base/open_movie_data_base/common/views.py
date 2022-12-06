from django.db.models import Count
from django.shortcuts import redirect, render
from django.views import generic as views

from open_movie_data_base.common.models import FavouriteMovies, ReviewLike, Review, Like
from open_movie_data_base.movie.models import Movie
from open_movie_data_base.utils.func import get_user_favourite_movies, get_review_set_likes, get_general_like


def dispatcher(request):
    current_user = request.user
    if current_user.is_movie_director and not current_user.moviedirector.movie_set.all():
        return redirect('add-movie')
    return redirect('home-page')


def get_latest_uploads():
    return Movie.objects.all().order_by('-uploaded_on')[:5]


class Index(views.ListView):
    model = Movie
    template_name = 'index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_uploads'] = get_latest_uploads()
        context['user_favourite_movies'] = get_user_favourite_movies(request=self.request)
        context['user_liked_movies'] = get_general_like(self.request)
        context['is_not_banned'] = True
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        genre = self.request.GET.get('genres')
        if genre:
            queryset = queryset.filter(genres__category__exact=genre)
        search_text = self.request.GET.get("searchbar")
        order_by = self.request.GET.get('filters')
        if order_by:

            if order_by in ['likes']:
                queryset = self.order_by_likes(queryset)

            elif order_by in ['rating']:
                queryset = self.order_by_rating(queryset)

            else:
                queryset = queryset.order_by(order_by)

        if search_text:
            return queryset.filter(title__icontains=search_text)

        return queryset

    def querystring_url(self):
        data = self.request.GET.copy()
        data.pop(self.page_kwarg, None)
        return data.urlencode()

    @staticmethod
    def order_by_likes(queryset):
        return queryset.annotate(likes=Count('like')).order_by('likes')

    @staticmethod
    def order_by_rating(queryset):
        return queryset.order_by('-averagereviewscore__score')


def movie_reviews(request, slug):
    movie = Movie.objects.filter(slug=slug).get()
    reviews = movie.review_set.all()
    review_like_set = get_review_set_likes(request)

    order_by = request.GET.get('order_by')
    if order_by:
        if order_by == 'likes':
            reviews = reviews.annotate(likes=Count('reviewlike')).order_by('-likes', '-posted_on')
        else:
            reviews = reviews.order_by(order_by)

    context = {
        'movie': movie,
        'reviews': reviews,
        'user_liked_reviews': review_like_set
    }
    return render(request, 'movie_reviews.html', context)


def general_movie_like(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    movie = Movie.objects.filter(pk=pk).get()
    liked_obj = Like.objects.filter(liked_movie_id=pk, user=request.user).first()

    if liked_obj:
        liked_obj.delete()

    else:
        like = Like(liked_movie=movie, user=request.user)
        like.save()
    referee = request.META.get('HTTP_REFERER')
    return redirect(referee)


def add_to_favourite_movies(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    movie = Movie.objects.filter(pk=pk).get()
    liked_obj = FavouriteMovies.objects.filter(like_obj_id=pk, user=request.user).first()

    if liked_obj:
        liked_obj.delete()

    else:
        like = FavouriteMovies(like_obj=movie, user=request.user)
        like.save()
    referee = request.META.get('HTTP_REFERER')
    return redirect(referee)


def movie_reviews_likes(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    review = Review.objects.filter(pk=pk).get()
    liked_obj = ReviewLike.objects.filter(like_obj_id=pk, user=request.user).first()

    if liked_obj:
        liked_obj.delete()

    else:
        like = ReviewLike(like_obj=review, user=request.user)
        like.save()
    referee = request.META.get('HTTP_REFERER')

    return redirect(referee + f'#{review.pk}')


def delete_movie_review(request, pk):
    review = Review.objects.filter(pk=pk).get()
    if request.user == review.user:
        review.delete()

    return redirect(request.META.get('HTTP_REFERER'))
