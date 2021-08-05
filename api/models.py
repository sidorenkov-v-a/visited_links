from django.db import models
from math import floor


class VisitedLink(models.Model):
    domain = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def timestamp(self):
        return floor(self.date.timestamp())
