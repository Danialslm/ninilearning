from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from apps.content.models import Serial, Movie, Episode
from apps.votes.models import Vote


class ExtraMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'bookmarked': self.get_bookmarked(),
            'liked': self.get_liked(),
            'disliked': self.get_disliked(),
        })
        return context

    def get_bookmarked(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_bookmarked(self.object)

    def get_liked(self):
        if self.request.user.is_authenticated:
            return self.object.liked(self.request.user)

    def get_disliked(self):
        if self.request.user.is_authenticated:
            return self.object.disliked(self.request.user)


class SeasonEpisodesMixin:
    def get_season_episodes(self, season):
        episodes = season.episodes.all()
        if self.request.user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Episode)
            episodes = episodes.annotate(
                is_liked=Q(
                    votes__user=self.request.user,
                    votes__vote=Vote.Choices.LIKE,
                    votes__object_id=F('id'),
                    votes__content_type=content_type,
                ),
                is_disliked=Q(
                    votes__user=self.request.user,
                    votes__vote=Vote.Choices.DISLIKE,
                    votes__object_id=F('id'),
                    votes__content_type=content_type,
                ),
            )
        return episodes


class SerialDetailView(ExtraMixin, SeasonEpisodesMixin, DetailView):
    template_name = 'content/detail/serial_detail.html'
    queryset = Serial.objects.prefetch_related('genres', 'suggestions__genres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first_season_episodes'] = self.get_first_season_episodes()
        return context

    def get_first_season_episodes(self):
        first_season = self.object.seasons.filter(season_number=1).get()
        return self.get_season_episodes(first_season)


class SeasonEpisodeListView(SeasonEpisodesMixin, ListView):
    template_name = 'content/detail/episode_list.html'
    context_object_name = 'episodes'

    def get_queryset(self):
        serial = get_object_or_404(Serial, slug=self.kwargs.get('slug'))
        season = get_object_or_404(serial.seasons, season_number=self.kwargs.get('season_number'))
        return self.get_season_episodes(season)


class MovieDetailView(ExtraMixin, DetailView):
    template_name = 'content/detail/movie_detail.html'
    queryset = Movie.objects.prefetch_related('genres', 'suggestions__genres')
