from django.contrib import admin

from open_movie_data_base.common.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['movie', 'rating', 'user', 'posted_on', ]
