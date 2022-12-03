# from django.db.models import signals
# from django.dispatch import receiver
# from django.utils.text import slugify
#
# from open_movie_data_base.common.models import AverageReviewScore
# from open_movie_data_base.movie.models import Movie
#
#
# @receiver(signals.post_save, sender=Movie)
# def append_movie_director_on_movie_creation(instance, *args, **kwargs):
#     if True:
#         AverageReviewScore(
#             movie=instance,
#         ).save()
#         instance.slug = slugify(f'{instance.title}-{instance.pk}')
