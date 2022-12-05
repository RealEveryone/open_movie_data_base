from django.db.models import signals
from django.dispatch import receiver

from open_movie_data_base.common.models import Review


def get_average_score(review_set):
    average_score = 0
    for review in review_set:
        average_score += review.rating
    if average_score > 0:
        return average_score / review_set.count()
    return 0


@receiver(signals.post_save, sender=Review)
def create_or_update_average_movie_score(instance, *args, **kwargs):
    movie = instance.movie
    review_set = movie.review_set.all()
    movie.averagereviewscore.score = get_average_score(review_set)
    movie.averagereviewscore.save()

# average_host.total_sum_of_numbers = average_host.total_sum_of_numbers + instance.rating
# average_host.save()
#
# average_host.score = average_host.total_sum_of_numbers / review_set_count
# average_host.save()
