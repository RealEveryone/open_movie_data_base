from django.db.models import signals
from django.dispatch import receiver

from open_movie_data_base.common.models import Review


@receiver(signals.post_save, sender=Review)
def create_or_update_average_movie_score(instance, *args, **kwargs):
    movie = instance.movie
    review_set_count = movie.review_set.all().count()
    average_host = movie.averagereviewscore

    average_host.total_sum_of_numbers = average_host.total_sum_of_numbers + instance.rating
    average_host.save()

    average_host.score = average_host.total_sum_of_numbers / review_set_count
    average_host.save()


