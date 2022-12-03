from django.db.models import Count
from django.shortcuts import redirect
from django.views import generic as views

from open_movie_data_base.common.models import Like
from open_movie_data_base.movie.models import Movie
from open_movie_data_base.utils.func import get_user_favourite_movies


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


# todo: When on 1+ and there no movie from the certain category gives an error


def like_func(request, pk):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    movie = Movie.objects.filter(pk=pk).get()
    liked_obj = Like.objects.filter(like_obj_id=pk, user=request.user).first()

    if liked_obj:
        liked_obj.delete()

    else:
        like = Like(like_obj=movie, user=request.user)
        like.save()
    referee = request.META.get('HTTP_REFERER')
    return redirect(referee)
