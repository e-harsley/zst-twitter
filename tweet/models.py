from django.db import models
from helpers.models import TrackingModel
from authentication.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class TweetMedia(TrackingModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    media = models.URLField()

    def __str__(self):
        return f"{self.user}'s tweet images"


class Tweets(TrackingModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    media_content = models.ManyToManyField(TweetMedia, related_name="media_contenr", blank=True)

    class Meta:
        verbose_name_plural = _('Tweets')

    def __str__(self):
        return f"{self.content} {self.user}"
