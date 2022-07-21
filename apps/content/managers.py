from datetime import timedelta

from django.db.models import Manager, QuerySet, Q
from django.utils import timezone


class ContentQueryset(QuerySet):
    def popular(self):
        """ Return objects that have more than or equal 50 popularity. """
        return self.filter(popularity__gte=50)

    def recent(self):
        """ Return contents that recently added. """
        now = timezone.now()
        start_time = now - timedelta(days=30)
        return self.filter(created_at__gte=start_time, created_at__lte=now)

    def search(self, search_query):
        return self.filter(
            Q(en_name__icontains=search_query) |
            Q(pe_name__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query)
        )


class ContentManager(Manager.from_queryset(ContentQueryset)):
    pass


class SerialManager(ContentManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(content_type=self.model.ContentTypeChoices.SERIAL)

    def create(self, **kwargs):
        kwargs['content_type'] = self.model.ContentTypeChoices.SERIAL
        return super().create(**kwargs)


class MovieManager(ContentManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(content_type=self.model.ContentTypeChoices.MOVIE)

    def create(self, **kwargs):
        kwargs['content_type'] = self.model.ContentTypeChoices.MOVIE
        return super().create(**kwargs)
