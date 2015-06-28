import json

from nose.tools import assert_equal, assert_true

from rest_framework.test import APITestCase
from django.contrib.auth.models import User


def decode(response):
    return json.loads(response.content.decode('utf-8'))


class TestCreateUserAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.all().delete()

    def _create_user(self, username):
        response = self.client.post(
            '/users/',
            data=json.dumps({"username": username}),
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_can_create_user_account(self):
        http_status, response_json = self._create_user('test_001')

        assert_equal(
            {
                "username": "test_001",
                "expected_daily_calories": 2000,
            },
            response_json)
        assert_equal(201, http_status)

        User.objects.get(username='test_001')

    def test_cannot_create_user_with_existing_username(self):
        http_status, response_json = self._create_user('test_002')
        assert_equal(201, http_status)

        http_status, response_json = self._create_user('test_002')
        assert_equal(400, http_status)
        assert_equal({'username': ['This field must be unique.']},
                     response_json)

    def test_new_users_have_sane_default_target_calories(self):
        self._create_user('test_003')
        user = User.objects.get(username='test_003')
        assert_equal(2000, user.user_profile.expected_daily_calories)

    def test_new_users_are_not_superuser(self):
        self._create_user('test_004')
        user = User.objects.get(username='test_004')
        assert_equal(False, user.is_superuser)

    def test_new_user_passwords_can_login(self):
        data = json.dumps({"username": "test_005", "password": "password_005"})

        response = self.client.post(
            '/users/',
            data=data,
            content_type='application/json')
        html_status, _ = (response.status_code, decode(response))
        assert_equal(201, html_status)

        assert_true(self.client.login(
            username='test_005', password='password_005'))


class TestRetrieveUserAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normal_1 = User.objects.create_user(username='normal_1')
        cls.normal_2 = User.objects.create_user(username='normal_2')
        cls.superuser_1 = User.objects.create_user(username='superuser_1')
        cls.superuser_1.is_superuser = True
        cls.superuser_1.save()

    def _get_user(self, username):
        response = self.client.get(
            '/users/{}/'.format(username),
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._get_user('normal_1')
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_normal_users_cannot_retrieve_other_users(self):
        self.client.force_authenticate(self.normal_2)
        http_status, response_json = self._get_user('normal_1')
        assert_equal(404, http_status)  # 404: others users are invisible

    def test_normal_users_can_retrieve_themselves(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._get_user('normal_1')

        assert_equal(
            {
                'username': 'normal_1',
                'expected_daily_calories': 2000
            },
            response_json)
        assert_equal(200, http_status)

    def test_superusers_can_retrieve_other_users(self):
        self.client.force_authenticate(self.superuser_1)
        http_status, response_json = self._get_user('normal_1')
        assert_equal(200, http_status)


class TestUpdateUserAccount(APITestCase):

    def _update_user(self, username, data):
        response = self.client.put(
            '/users/{}/'.format(username),
            data=json.dumps(data),
            content_type='application/json')
        return (response.status_code, decode(response))

    @classmethod
    def setUpTestData(cls):
        cls.normal_1 = User.objects.create_user(username='normal_1')
        cls.normal_2 = User.objects.create_user(username='normal_2')
        cls.superuser_1 = User.objects.create_user(username='superuser_1')
        cls.superuser_1.is_superuser = True
        cls.superuser_1.save()

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._update_user(
            'normal_1',
            {
                'username': 'normal_1',
                'expected_daily_calories': 1000
            }
        )
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_normal_users_cannot_update_other_users(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._update_user(
            'normal_2',
            {
                'username': 'normal_2',
                'expected_daily_calories': 1000
            }
        )
        assert_equal(404, http_status)  # 404: others users are invisible

    def test_normal_users_can_update_themselves(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._update_user(
            'normal_1',
            {
                'username': 'normal_1',
                'expected_daily_calories': 1000
            }
        )
        assert_equal(200, http_status)

    def test_that_expected_daily_calories_can_be_omitted(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._update_user(
            'normal_1',
            {
                'username': 'normal_1',
            }
        )
        assert_equal(200, http_status)

    def test_that_updates_actually_persist(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._update_user(
            'normal_1',
            {
                'username': 'normal_1',
                'expected_daily_calories': 999
            }
        )

        user = User.objects.get(username='normal_1')
        assert_equal(
            999,
            user.user_profile.expected_daily_calories)

    def test_superusers_can_update_other_users(self):
        self.client.force_authenticate(self.superuser_1)
        http_status, response_json = self._update_user(
            'normal_1',
            {
                'username': 'normal_1',
                'expected_daily_calories': 1000
            }
        )
        assert_equal(200, http_status)


class TestDeleteUserAccount(APITestCase):
    def setUp(cls):  # Do this before every test as we are deleting
        cls.normal_1 = User.objects.create_user(username='normal_1')
        cls.normal_2 = User.objects.create_user(username='normal_2')
        cls.superuser_1 = User.objects.create_user(username='superuser_1')
        cls.superuser_1.is_superuser = True
        cls.superuser_1.save()

    def _delete_user(self, username):
        response = self.client.delete(
            '/users/{}/'.format(username),
            content_type='application/json')

        if response.status_code != 204:  # HTTP 204 No Content
            json_response = decode(response)
        else:
            json_response = None

        return (response.status_code, json_response)

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._delete_user('normal_1')
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_normal_users_cannot_delete_other_users(self):
        self.client.force_authenticate(self.normal_2)
        http_status, response_json = self._delete_user('normal_1')
        assert_equal(404, http_status)  # 404: others users are invisible

    def test_normal_users_can_delete_themselves(self):
        self.client.force_authenticate(self.normal_1)
        http_status, response_json = self._delete_user('normal_1')

        assert_equal(204, http_status)  # HTTP 204 No Content

    def test_superusers_can_delete_other_users(self):
        self.client.force_authenticate(self.superuser_1)
        http_status, response_json = self._delete_user('normal_1')
        assert_equal(204, http_status)

    def test_deleted_users_are_actually_deleted(self):
        assert_equal(1, User.objects.filter(username='normal_1').count())

        self.client.force_authenticate(self.normal_1)
        self._delete_user('normal_1')

        assert_equal(0, User.objects.filter(username='normal_1').count())
