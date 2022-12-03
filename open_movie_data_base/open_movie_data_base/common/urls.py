from django.urls import path

from open_movie_data_base.common.views import *

urlpatterns = [
    path('home/', Index.as_view(), name='home-page'),
    path('redirect-to/', dispatcher, name='dispatcher'),
    # path('load-more-reviews/', lazy_load_posts, name='load-more-posts')
    # path('api/reviews', ReviewListView.as_view(), name='comments-api')

]

from .signals import *
