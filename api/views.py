from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError
from .models import VisitedLink
from datetime import datetime, timezone


class VisitedLinksView(APIView):
    def post(self, request):
        domains = self.parse_request(request)
        for domain in domains:
            VisitedLink.objects.create(domain=domain)
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
        domains = VisitedLink.objects.filter(
            date__range=[date_from, date_to]).values_list('domain', flat=True)
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
        date_from = datetime.fromtimestamp(int(date_from), timezone.utc)
        date_to = datetime.fromtimestamp(int(date_to) + 1, timezone.utc)
        return date_from, date_to
