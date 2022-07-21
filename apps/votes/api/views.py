from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from apps.content.models import Content, Episode


class VoteMixin:
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        vote = self.request.GET.get('vote')
        if vote == 'like':
            self.object.add_like(self.request.user)
            return Response()
        elif vote == 'dislike':
            self.object.add_dislike(self.request.user)
            return Response()
        else:
            return Response(
                {'detail': _('Please provide `vote` querystring with `like` or `dislike` value.')},
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete_vote(self.request.user)
        return Response(status=HTTP_204_NO_CONTENT)


class ContentVoteAPIView(VoteMixin, GenericAPIView):
    queryset = Content.objects.all()
    lookup_field = 'slug'


class EpisodeVoteAPIView(VoteMixin, GenericAPIView):
    queryset = Episode.objects.all()
