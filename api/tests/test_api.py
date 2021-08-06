from api.models import VisitedLink
from api.views import redis
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .common import create_client_data, create_data_for_db


class TestApi:
    links_url = reverse('visited_links')
    domains_url = reverse('visited_domains')
    client = APIClient()

    def test_visited_links(self):
        response = self.client.get(self.links_url)
        assert response.status_code != 404, (
            f'{self.links_url} should be available',
            response.json()
        )

        assert VisitedLink.objects.count() == 0

        data = create_client_data()
        response = self.client.post(self.links_url, data, format='json')
        assert response.status_code == 200, (
            'Client should be able to post valid links',
            response.json()
        )
        assert VisitedLink.objects.count() == 3

    def test_visited_domains(self):
        redis.flushall()

        links_1, timestamp_1 = create_data_for_db()
        links_2, timestamp_2 = create_data_for_db(add_seconds=10)

        for link in links_1:
            VisitedLink.objects.create(**link)

        for link in links_2:
            VisitedLink.objects.create(**link)

        params = {'from': timestamp_1, 'to': timestamp_2}
        response = self.client.get(self.domains_url, params)
        assert response.status_code == 200, (
            'Client should be able to get valid links',
            response.json()
        )

        result_set = set(response.data['domains'])
        set_links_1 = {x['domain'] for x in links_1}
        set_links_2 = {x['domain'] for x in links_2}

        assert set_links_1.issubset(result_set), (
            'Some domains not in result',
            response.json()
        )
        assert set_links_2.issubset(result_set), (
            'Some domains not in result',
            response.json()
        )

        params = {'from': timestamp_1 + 9, 'to': timestamp_2}
        response = self.client.get(self.domains_url, params)
        result_set = set(response.data['domains'])
        assert not set_links_1.issubset(result_set), (
            f'Domains {set_links_1} should not be in result {result_set}',
            response.json()
        )
        assert set_links_2.issubset(result_set), (
            f'Domains {set_links_2} not in result {result_set}',
            response.json()
        )
