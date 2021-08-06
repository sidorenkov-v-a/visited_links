from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from .common import create_client_data, create_data_for_db
from api.models import VisitedLink
from api.views import redis


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

# from rest_framework.reverse import reverse
# from rest_framework.test import APIClient
# from polls.models import Poll
# from django.contrib.auth import get_user_model
# from .common import create_poll_data
#
#
# class TestPoll:
#     url_list = reverse('poll-list')
#
#     @property
#     def url_detail(self, pk=1):
#         return reverse('poll-detail', kwargs={'pk': pk})
#
#     def test_user_get(self, user_client: APIClient):
#         response = user_client.get(self.url_list)
#         assert response.status_code == 200, (
#             'User should be able to get poll list. ',
#             response.json()
#         )
#
#     def test_admin_get(self, admin_client: APIClient):
#         response = admin_client.get(self.url_list)
#         assert response.status_code == 200, (
#             'Admin user should be able to get poll list. ',
#             response.json()
#         )
#
#     def test_user_create(self, user_client: APIClient):
#         assert Poll.objects.count() == 0
#         data = create_poll_data()
#         response = user_client.post(self.url_list, data)
#         assert response.status_code == 401, (
#             'User should NOT be able to create poll',
#             response.json()
#         )
#         assert Poll.objects.count() == 0
#
#     def test_admin_create(self, admin_client: APIClient):
#         assert Poll.objects.count() == 0
#         data = create_poll_data()
#         response = admin_client.post(self.url_list, data)
#         assert response.status_code == 201, (
#             'User should be able to create poll',
#             response.json()
#         )
#         assert Poll.objects.count() == 1
#         poll = Poll.objects.get(pk=1)
#         assert poll.title == data['title']
#         assert poll.description == data['description']
#         assert poll.date_start.strftime('%Y-%m-%d') == data['date_start']
#         assert poll.date_end.strftime('%Y-%m-%d') == data['date_end']
#
#     def test_user_update(self, user_client: APIClient):
#         data = create_poll_data()
#         Poll.objects.create(**data)
#         assert Poll.objects.count() == 1
#         response = user_client.patch(self.url_detail, {'title': 'New title'})
#         assert response.status_code == 401, (
#             'User should NOT be able to update poll',
#             response.json()
#         )
#         response = user_client.put(self.url_detail, data)
#         assert response.status_code == 401, (
#             'User should NOT be able to update poll',
#             response.json()
#         )
#
#     def test_admin_update(self, admin_client: APIClient):
#         data = create_poll_data()
#         Poll.objects.create(**data)
#         assert Poll.objects.count() == 1
#         response = admin_client.patch(self.url_detail, {'title': 'New title'})
#         assert response.status_code == 200, (
#             'Admin should be able to update poll',
#             response.json()
#         )
#         response = admin_client.put(self.url_detail, data)
#         assert response.status_code == 200, (
#             'Admin should be able to update poll',
#             response.json()
#         )
#
#     def test_time(self, admin_client: APIClient):
#         from datetime import datetime, timedelta
#         date_start = datetime.today()
#         date_end = datetime.today() - timedelta(days=1)
#         data = create_poll_data(date_start=date_start, date_end=date_end)
#
#         response = admin_client.post(self.url_list, data)
#         assert response.status_code == 400, (
#             'Date end should be greater than date start',
#             response.json()
#         )
#
#         data = create_poll_data()
#         Poll.objects.create(**data)
#         response = admin_client.patch(
#             self.url_detail,
#             {'date_start': date_start, 'date_end': date_end}
#         )
#         assert response.status_code == 400, (
#             'Date end should be greater than date start',
#             response.json()
#         )
#
#         response = admin_client.patch(
#             self.url_detail,
#             {'date_end': date_end}
#         )
#         assert response.status_code == 400, (
#             'Date end should be greater than date start',
#             response.json()
#         )
#
#         # ///Can not change start date after creat
#
#
#
#
#
#
