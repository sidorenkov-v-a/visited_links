from django.contrib import admin
from .models import VisitedLink


class VisitedLinkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'domain', 'date', 'timestamp')


admin.site.register(VisitedLink, VisitedLinkAdmin)
