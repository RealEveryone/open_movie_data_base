from django.views.decorators.cache import cache_page


class ChoicesMixin:

    @classmethod
    def get_choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def get_length(cls):
        return max(len(choice) for _, choice in cls.get_choices())


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)


class RemoveFiltersFormNavMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_banned'] = True

        return context

