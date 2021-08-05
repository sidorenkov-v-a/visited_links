from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError
from .models import VisitedLink
from datetime import datetime, timezone
from django.conf import settings
from django.shortcuts import redirect

from redis import Redis

REDIS_HOST = settings.REDIS['default']['HOST']
REDIS_PORT = settings.REDIS['default']['PORT']
redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


class VisitedLinksView(APIView):
    def post(self, request):
        domains = self.parse_request(request)
        for domain in domains:
            link = VisitedLink.objects.create(domain=domain)

            time_stamp = round(datetime.now().timestamp())
            redis.zadd('links', {f'{link.domain}:{link.id}': time_stamp})
        return Response({'status': 'ok'})

    def parse_request(self, request):
        try:
            urls = request.data['links']
        except KeyError:
            raise ValidationError({'links': 'This field is required'})
        domains = set()
        for url in urls:
            parsed_uri = urlparse(url)
            if parsed_uri.netloc:
                result = parsed_uri.netloc
            else:
                result = parsed_uri.path
            domains.add(result)
        return domains


class VisitedDomainsView(APIView):

    def get(self, request):
        date_from, date_to = self.parse_request(request)
        domains = self.get_from_cache(date_from, date_to)
        if not domains:
            links = self.get_from_db(date_from, date_to)
            self.update_cache(links)
            domains = links.distinct().values_list('domain', flat=True)

        return Response({'status': 'ok', 'domains': domains})

    def parse_request(self, request):
        date_from = request.GET.get('from', None)
        date_to = request.GET.get('to', None)
        errors = {}
        if not date_from:
            errors['from'] = 'This query param is required'
        if not date_to:
            errors['to'] = 'This query param is required'
        if errors:
            raise ValidationError(errors)

        return date_from, date_to

    def get_from_cache(self, date_from, date_to):
        raw_domains = redis.zrangebyscore('links', date_from, date_to)
        domains = set()
        for raw_domain in raw_domains:
            domain = raw_domain.decode('utf-8').split(':')[0]
            domains.add(domain)
        return domains

    def get_from_db(self, date_from, date_to):
        date_from = datetime.fromtimestamp(int(date_from), timezone.utc)
        date_to = datetime.fromtimestamp(int(date_to) + 1, timezone.utc)

        domains = VisitedLink.objects.filter(
            date__range=[date_from, date_to]
        )
        return domains

    def update_cache(self, links):
        for link in links:
            redis.zadd('links', {f'{link.domain}:{link.id}': link.timestamp})


# def index(request):
#     return redirect('visited_links')
