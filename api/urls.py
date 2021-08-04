from django.urls import path
from .views import VisitedLinksView, VisitedDomainsView

urlpatterns = [
    path('visited_links/', VisitedLinksView.as_view(), name='visited_links'),
    path(
        'visited_domains/',
        VisitedDomainsView.as_view(),
        name='visited_domains'
    )
]
