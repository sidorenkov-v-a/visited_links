from django.db import models


class VisitedLink(models.Model):
    domain = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def timestamp(self):
        return int(self.date.timestamp())


