from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class Vote(models.Model):
    class Choices(models.IntegerChoices):
        LIKE = 1, _('like')
        DISLIKE = -1, _('dislike')

    vote = models.SmallIntegerField(_('vote'), choices=Choices.choices)
    user = models.ForeignKey(
        'users.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='votes',
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(_('object id'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        unique_together = ('user', 'content_type', 'object_id')


class VoteMixin(models.Model):
    votes = GenericRelation(Vote)
    likes_count = models.PositiveSmallIntegerField(_('likes count'), default=0, editable=False)
    dislikes_count = models.PositiveSmallIntegerField(_('dislikes count'), default=0, editable=False)
    popularity = models.PositiveSmallIntegerField(
        _('popularity'),
        default=0,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        total_votes = self.total_votes
        self.popularity = int(self.likes_count * 100 / total_votes) if total_votes > 0 else 0
        super().save(*args, **kwargs)

    @property
    def total_votes(self):
        return self.likes_count + self.dislikes_count

    @property
    def _general_vote_query_data(self):
        return {
            'content_type': ContentType.objects.get_for_model(self),
            'object_id': self.id,
        }

    def add_like(self, user):
        vote = self.votes.filter(
            Q(vote=Vote.Choices.LIKE) | Q(vote=Vote.Choices.DISLIKE),
            user=user,
            **self._general_vote_query_data,
        ).only('vote').first()

        if vote:
            if vote.vote == Vote.Choices.LIKE:
                return
            else:
                vote.vote = Vote.Choices.LIKE
                vote.save(update_fields=['vote'])
                self.dislikes_count -= 1
        else:
            self.votes.create(
                vote=Vote.Choices.LIKE,
                user=user,
                **self._general_vote_query_data,
            )
        self.likes_count += 1
        self.save(update_fields=['likes_count', 'dislikes_count', 'popularity'])

    def add_dislike(self, user):
        vote = self.votes.filter(
            Q(vote=Vote.Choices.LIKE) | Q(vote=Vote.Choices.DISLIKE),
            user=user,
            **self._general_vote_query_data,
        ).only('vote').first()

        if vote:
            if vote.vote == Vote.Choices.DISLIKE:
                return
            else:
                vote.vote = Vote.Choices.DISLIKE
                vote.save(update_fields=['vote'])
                self.likes_count -= 1
        else:
            self.votes.create(
                vote=Vote.Choices.DISLIKE,
                user=user,
                **self._general_vote_query_data,
            )
        self.dislikes_count += 1
        self.save(update_fields=['likes_count', 'dislikes_count', 'popularity'])

    def delete_vote(self, user):
        vote = self.votes.filter(
            Q(vote=Vote.Choices.LIKE) | Q(vote=Vote.Choices.DISLIKE),
            user=user,
            **self._general_vote_query_data,
        ).first()
        if not vote:
            return

        vote.delete()
        if vote.vote == Vote.Choices.LIKE:
            self.likes_count -= 1
        else:
            self.dislikes_count -= 1
        self.save()

    def liked(self, user):
        return self.votes.filter(
            vote=Vote.Choices.LIKE,
            user=user,
            **self._general_vote_query_data,
        ).exists()

    def disliked(self, user):
        return self.votes.filter(
            vote=Vote.Choices.DISLIKE,
            user=user,
            **self._general_vote_query_data,
        ).exists()
