import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass




# import pytest
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
#
#
# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass
#
#
# @pytest.fixture
# def admin_client():
#     admin = get_user_model().objects.create_superuser(
#         username='TestUser', email='TestUser@TestUser.fake', password='1234567'
#     )
#     client = APIClient()
#     client.force_authenticate(user=admin)
#     return client
#
#
# @pytest.fixture
# def user_client():
#     client = APIClient()
#     return client
#
#
