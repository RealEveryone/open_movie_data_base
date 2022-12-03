from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('open_movie_data_base.user.urls')),
    path('movie/', include('open_movie_data_base.movie.urls')),
    path('', include('open_movie_data_base.common.urls'))
]
