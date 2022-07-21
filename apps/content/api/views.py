from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import Content


class BookmarkAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Content, slug=self.kwargs.get('slug'))
        self.request.user.bookmarks.add(self.object)
        return Response({'detail': _('The object is bookmarked.')})

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(Content, slug=self.kwargs.get('slug'))
        self.request.user.bookmarks.remove(self.object)
        return Response({'detail': _('The object bookmark deleted.')})
