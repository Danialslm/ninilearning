from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from apps.content.models import Content, Genre
from apps.core.mixins import OrderingMixin
from .models import Slide, Collection


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'slides': Slide.objects.all(),
            'popular': Content.objects.prefetch_related('genres').popular()[:8],
            'recent': Content.objects.prefetch_related('genres').recent()[:8],
            'collections': self.get_first_collections_page()
        })
        return context

    def get_first_collections_page(self):
        collections = Collection.objects.prefetch_related('contents', 'contents__genres')
        collections_paginator = Paginator(collections, 8)
        return collections_paginator.get_page(1)


class CollectionListView(ListView):
    template_name = 'pages/collection_list.html'
    queryset = Collection.objects.prefetch_related('contents', 'genres')
    context_object_name = 'collections'
    paginate_by = 8


class CollectionContentListView(OrderingMixin, ListView):
    template_name = 'pages/content_list/collection_content_list.html'
    paginate_by = 20

    def get_queryset(self):
        collection = get_object_or_404(
            Collection.objects.prefetch_related(
                Prefetch('contents', Content.objects.order_by(self.ordering)),
                'contents__genres'
            ),
            slug=self.kwargs.get('slug'),
        )
        return collection.contents.all()


class RecentContentListView(OrderingMixin, ListView):
    template_name = 'pages/content_list/recent.html'
    queryset = Content.objects.prefetch_related('genres').recent()
    paginate_by = 20


class PopularContentListView(OrderingMixin, ListView):
    template_name = 'pages/content_list/popular.html'
    queryset = Content.objects.prefetch_related('genres').popular()
    paginate_by = 20


class GenreContentListView(OrderingMixin, ListView):
    template_name = 'pages/content_list/genre_content_list.html'
    paginate_by = 20

    def get_queryset(self):
        genre = get_object_or_404(
            Genre.objects.prefetch_related(
                Prefetch('contents', Content.objects.order_by(self.ordering)),
                'contents__genres',
            ),
            genre=self.kwargs.get('genre')
        )
        return genre.contents.all()


class SearchResultListView(ListView):
    def get_template_names(self):
        if self.request.GET.get('query') is None:
            return ['pages/search/form.html']
        return ['pages/search/results.html']

    def get_queryset(self):
        query = self.request.GET.get('query')
        if not query:
            return []
        return Content.objects.prefetch_related('genres').search(query)
