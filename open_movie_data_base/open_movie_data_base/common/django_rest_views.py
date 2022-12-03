from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.template import loader
from rest_framework import serializers
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from open_movie_data_base.common.models import Review


class CustomPaginatorClass(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'review']


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPaginatorClass

    def list(self, request, *args, **kwargs):
        context = super().list(*args, **kwargs)
        context['reviews_html'] = loader.render_to_string(
            'movie/partials/reviews_partial.html',
            {'reviews': self.queryset}
        )
        return context


def lazy_load_posts(request):
    page = request.POST.get('page')
    reviews = Review.objects.all()

    results_per_page = 5
    paginator = Paginator(reviews, results_per_page)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(2)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    # build a html posts list with the paginated posts
    reviews_html = loader.render_to_string(
        'movie/partials/reviews_partial.html',
        {'posts': reviews}
    )
    # package output data and return it as a JSON object
    output_data = {
        'posts_html': reviews_html,
        'has_next': reviews.has_next()
    }
    return JsonResponse(output_data)
