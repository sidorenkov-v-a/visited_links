from math import floor

from django.db import models


class VisitedLink(models.Model):
    domain = models.CharField(max_length=100)
    date = models.DateTimeField()

    @property
    def timestamp(self):
        return floor(self.date.timestamp())
