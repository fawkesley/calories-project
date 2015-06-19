import json

from nose.tools import assert_equal

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.meals.models import Meal

MEAL_1 = {
        'date': '2015-01-01',
        'time': '09:00:00',
        'description': 'Avocado and bacon salad.',
        'calories': 400
    }

MEAL_2 = {
        'date': '2015-01-01',
        'time': '09:00:00',
        'description': 'Mcflurry.',
        'calories': 800
    }


def decode(response):
    return json.loads(response.content.decode('utf-8'))


class UsersMealsDataMixin(object):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user_1')
        cls.user_2 = User.objects.create(username='user_2')
        cls.superuser = User.objects.create_user(username='superuser')
        cls.superuser.is_superuser = True
        cls.superuser.save()

        Meal.objects.create(owner=cls.user_1, **MEAL_1)
        Meal.objects.create(owner=cls.user_1, **MEAL_2)


class TestCreateMeal(UsersMealsDataMixin, APITestCase):
    def _create_meal(self, username, args):
        response = self.client.post(
            '/users/{username}/meals/'.format(username=username),
            data=json.dumps(args),
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_unauthenticated_request_is_rejected(self):
        http_status, response_json = self._create_meal('user_1', MEAL_1)
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_user_1_can_create_meal_for_themselves(self):
        self.client.force_authenticate(self.user_1)

        http_status, response_json = self._create_meal('user_1', MEAL_1)
        assert_equal(201, http_status)

    def test_created_meal_is_actually_persisted(self):
        self.client.force_authenticate(self.user_1)

        Meal.objects.all().delete()
        http_status, response_json = self._create_meal('user_1', MEAL_1)
        assert_equal(1, Meal.objects.all().count())

    def test_user_1_cannot_create_meal_for_user_2(self):
        self.client.force_authenticate(self.user_1)

        http_status, response_json = self._create_meal('user_2', MEAL_1)
        assert_equal(403, http_status)
        assert_equal(
            {'detail': 'You do not have permission to perform this action.'},
            response_json)

    def test_superuser_can_create_meal_user_1(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._create_meal('user_1', MEAL_1)
        assert_equal(201, http_status)

    def test_meal_created_by_superuser_is_owned_by_target_user(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._create_meal('user_1', MEAL_1)
        assert_equal(201, http_status)
        pk = response_json['id']
        assert_equal(
            self.user_1,
            Meal.objects.get(pk=pk).owner)


class TestRetrieveMeal(UsersMealsDataMixin, APITestCase):
    @classmethod
    def setUpTestData(cls):
        super(TestRetrieveMeal, cls).setUpTestData()

    def _get_meal(self, username, meal_id):
        response = self.client.get(
            '/users/{0}/meals/{1}/'.format(username, meal_id),
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._get_meal('user_1', 1)
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_user_2_cannot_retrieve_a_meal_belonging_to_user_1(self):
        self.client.force_authenticate(self.user_2)
        http_status, response_json = self._get_meal('user_1', 1)
        assert_equal(403, http_status)

    def test_normal_users_can_retrieve_their_own_meal(self):
        self.client.force_authenticate(self.user_1)
        http_status, response_json = self._get_meal('user_1', 1)

        assert_equal(
            {
                'calories': 400,
                'date': '2015-01-01',
                'description': 'Avocado and bacon salad.',
                'id': 1,
                'time': '09:00:00'
            },
            response_json)
        assert_equal(200, http_status)

    def test_superusers_can_retrieve_other_users(self):
        self.client.force_authenticate(self.superuser)
        http_status, response_json = self._get_meal('user_1', 1)
        assert_equal(200, http_status)


class TestUpdateMeal(UsersMealsDataMixin, APITestCase):

    def _update_meal(self, username, meal_id, data):
        response = self.client.put(
            '/users/{0}/meals/{1}/'.format(username, meal_id),
            data=json.dumps(data),
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._update_meal(
            'user_1', 1, MEAL_2)
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_user_2_cannot_update_a_meal_belonging_to_user_1(self):
        self.client.force_authenticate(self.user_2)
        http_status, response_json = self._update_meal(
            'user_1', 1, MEAL_2)
        assert_equal(403, http_status)

    def test_normal_users_can_update_their_own_meal(self):
        self.client.force_authenticate(self.user_1)
        http_status, response_json = self._update_meal(
            'user_1', 1, MEAL_2)
        assert_equal(200, http_status)

    def test_that_updates_actually_persist(self):
        self.client.force_authenticate(self.user_1)
        http_status, response_json = self._update_meal(
            'user_1', 1,
            {
                'date': '2015-01-01',
                'time': '09:00:00',
                'description': 'Something REALLY big.',
                'calories': 20000
            }
        )

        meal = Meal.objects.get(pk=1)
        assert_equal(20000, meal.calories)

    def test_superusers_can_update_other_users(self):
        self.client.force_authenticate(self.superuser)
        http_status, response_json = self._update_meal(
            'user_1', 1, MEAL_2)
        assert_equal(200, http_status)


class TestDeleteMeal(UsersMealsDataMixin, APITestCase):
    def setUp(self):  # Do this before every test as we are deleting
        print('setUp')
        Meal.objects.all().delete()
        self.meal_1 = Meal.objects.create(owner=self.user_1, **MEAL_1)
        self.meal_2 = Meal.objects.create(owner=self.user_1, **MEAL_2)

    def _delete_meal(self, username, meal_id):
        response = self.client.delete(
            '/users/{0}/meals/{1}/'.format(username, meal_id),
            content_type='application/json')

        if response.status_code != 204:  # HTTP 204 No Content
            json_response = decode(response)
        else:
            json_response = None

        return (response.status_code, json_response)

    def test_unauthenticated_requests_fail(self):
        http_status, response_json = self._delete_meal(
            'user_1', self.meal_1.pk)
        assert_equal(401, http_status)
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)

    def test_normal_users_cannot_delete_other_user_meals(self):
        self.client.force_authenticate(self.user_2)
        http_status, response_json = self._delete_meal(
            'user_1', self.meal_1.pk)
        assert_equal(403, http_status)

    def test_users_can_delete_their_own_meals(self):
        self.client.force_authenticate(self.user_1)
        http_status, response_json = self._delete_meal(
            'user_1', self.meal_1.pk)

        assert_equal(204, http_status)  # HTTP 204 No Content

    def test_superusers_can_delete_other_users_meals(self):
        self.client.force_authenticate(self.superuser)
        http_status, response_json = self._delete_meal(
            'user_1', self.meal_1.pk)
        assert_equal(204, http_status)

    def test_deleted_meals_are_actually_deleted(self):
        def count_meals():
            return Meal.objects.all().count()

        assert_equal(2, count_meals())

        self.client.force_authenticate(self.user_1)
        http_status, _ = self._delete_meal('user_1', self.meal_1.pk)
        assert_equal(204, http_status)

        assert_equal(1, count_meals())
