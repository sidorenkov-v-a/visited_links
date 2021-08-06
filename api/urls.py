from django.urls import path

from .views import VisitedDomainsView, VisitedLinksView, index

urlpatterns = [
    path('visited_links/', VisitedLinksView.as_view(), name='visited_links'),
    path(
        'visited_domains/',
        VisitedDomainsView.as_view(),
        name='visited_domains'
    ),
    path('', index, name='index')
]
