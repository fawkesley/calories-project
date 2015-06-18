import json

from nose.tools import assert_equal, assert_in

from django.test import TestCase
from django.contrib.auth.models import User

from freezegun import freeze_time
from rest_framework_jwt.utils import jwt_decode_handler


def decode(response):
    return json.loads(response.content.decode('utf-8'))


class TestLogin(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.all().delete()
        User.objects.create_user(
            username='user_001', password='correct_password')

    def _post(self, url, data):
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json')
        return response.status_code, decode(response)

    @freeze_time('2015-01-01T00:00:00Z')
    def test_can_login_and_get_token(self):
        (http_status, response_json) = self._post(
            '/api-token-auth/',
            {'username': 'user_001',
             'password': 'correct_password'})

        assert_equal(200, http_status)
        assert_in('token', response_json)
        decoded_token = jwt_decode_handler(response_json['token'])
        assert_equal({
            'email': '',
            'exp': 1420156800,
            'user_id': 1,
            'username': 'user_001'},
            decoded_token)

    def test_incorrect_password_cannot_login(self):
        (http_status, response_json) = self._post(
            '/api-token-auth/',
            {'username': 'user_001',
             'password': 'wrong_password'})

        assert_equal(400, http_status)
        assert_equal({
            "non_field_errors": [
                "Unable to login with provided credentials."
                ]
            },
            response_json)
