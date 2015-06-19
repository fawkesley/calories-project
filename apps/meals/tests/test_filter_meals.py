import json

from nose.tools import assert_equal

from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from apps.meals.models import Meal


USER_1_MEALS = [
    {
        'date': '2015-01-01',
        'time': '09:00',
        'description': 'Avocado and bacon salad.',
        'calories': 400
    },
    {
        'date': '2015-01-01',
        'time': '13:00',
        'description': 'Poached eggs on toast.',
        'calories': 350
    },
    {
        'date': '2015-01-01',
        'time': '19:30',
        'description': 'Spaghetti carbonara.',
        'calories': 800
    },
    {
        'date': '2015-01-02',
        'time': '09:01',
        'description': 'Porridge with chia seeds.',
        'calories': 350
    },
    {
        'date': '2015-01-02',
        'time': '13:01',
        'description': 'Prawn salad.',
        'calories': 400
    },
    {
        'date': '2015-01-02',
        'time': '19:31',
        'description': 'Tagliatelle.',
        'calories': 780
    },
]

USER_2_MEALS = [
    {
        'date': '2015-01-01',
        'time': '08:00',
        'description': 'McFlurry and Mcdonalds Milkshake.',
        'calories': 1200
    },
    {
        'date': '2015-01-01',
        'time': '13:00',
        'description': 'Burger kind mega triple cheese bazinga.',
        'calories': 350
    },
    {
        'date': '2015-01-01',
        'time': '19:30',
        'description': 'Dominos Pizza.',
        'calories': 1000
    },
]


def decode(response):
    return json.loads(response.content.decode('utf-8'))


class TestFilterMeals(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user_1')
        cls.user_2 = User.objects.create(username='user_2')
        cls.superuser = User.objects.create_user(username='superuser')
        cls.superuser.is_superuser = True
        cls.superuser.save()

        for meal in USER_1_MEALS:
            Meal.objects.create(owner=cls.user_1, **meal)

        for meal in USER_2_MEALS:
            Meal.objects.create(owner=cls.user_2, **meal)

    def _get(self, url):
        response = self.client.get(
            url,
            content_type='application/json')
        return (response.status_code, decode(response))

    def test_that_meals_have_been_created(self):
        assert_equal(9, Meal.objects.all().count())

    def test_that_unauthenticated_request_not_allowed(self):
        http_status, response_json = self._get('/users/user_1/meals/')
        assert_equal(
            {'detail': 'Authentication credentials were not provided.'},
            response_json)
        assert_equal(401, http_status)

    def test_that_user_1_only_sees_their_own_meals(self):
        self.client.force_authenticate(self.user_1)

        http_status, response_json = self._get('/users/user_1/meals/')
        assert_equal(6, len(response_json))
        assert_equal(200, http_status)

    def test_that_user_1_cannot_see_user_2_meals(self):
        self.client.force_authenticate(self.user_1)

        http_status, response_json = self._get('/users/user_2/meals/')
        assert_equal(403, http_status)
        assert_equal(
            {'detail': 'You do not have permission to perform this action.'},
            response_json)

    def test_that_superuser_can_see_user_1_meals(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get('/users/user_1/meals/')
        assert_equal(6, len(response_json))
        assert_equal(200, http_status)

    def test_that_filter_from_date_excludes_dates_before(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
            '/users/user_1/meals/?from_date=2015-01-02')
        assert_equal(3, len(response_json))
        assert_equal([
            {
                'calories': 350,
                'date': '2015-01-02',
                'description': 'Porridge with chia seeds.',
                'id': 4,
                'time': '09:01:00'},
            {
                'calories': 400,
                'date': '2015-01-02',
                'description': 'Prawn salad.',
                'id': 5,
                'time': '13:01:00'},
            {
                'calories': 780,
                'date': '2015-01-02',
                'description': 'Tagliatelle.',
                'id': 6,
                'time': '19:31:00'}
        ],
            response_json)

    def test_that_filter_to_date_excludes_dates_after_inclusively(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
            '/users/user_1/meals/?to_date=2015-01-01')
        assert_equal(3, len(response_json))
        assert_equal([
            {
                'calories': 400,
                'date': '2015-01-01',
                'description': 'Avocado and bacon salad.',
                'id': 1,
                'time': '09:00:00'},
            {
                'calories': 350,
                'date': '2015-01-01',
                'description': 'Poached eggs on toast.',
                'id': 2,
                'time': '13:00:00'},
            {
                'calories': 800,
                'date': '2015-01-01',
                'description': 'Spaghetti carbonara.',
                'id': 3,
                'time': '19:30:00'}],
            response_json)

    def test_that_filter_same_to_and_from_date_includes_that_date(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
            '/users/user_1/meals/?to_date=2015-01-01&from_date=2015-01-01')
        assert_equal(3, len(response_json))

    def test_that_filter_from_time_excludes_times_before(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
            '/users/user_1/meals/?from_time=11:30')
        assert_equal(4, len(response_json))
        assert_equal([
            {
                'calories': 350,
                'date': '2015-01-01',
                'description': 'Poached eggs on toast.',
                'id': 2,
                'time': '13:00:00'},
            {
                'calories': 800,
                'date': '2015-01-01',
                'description': 'Spaghetti carbonara.',
                'id': 3,
                'time': '19:30:00'},
            {
                'calories': 400,
                'date': '2015-01-02',
                'description': 'Prawn salad.',
                'id': 5,
                'time': '13:01:00'},
            {
                'calories': 780,
                'date': '2015-01-02',
                'description': 'Tagliatelle.',
                'id': 6,
                'time': '19:31:00'},
        ],
            response_json)

    def test_that_filter_to_time_excludes_times_after(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
            '/users/user_1/meals/?to_time=11:30')
        assert_equal(2, len(response_json))
        assert_equal([
            {
                'calories': 400,
                'date': '2015-01-01',
                'description': 'Avocado and bacon salad.',
                'id': 1,
                'time': '09:00:00'},
            {
                'calories': 350,
                'date': '2015-01-02',
                'description': 'Porridge with chia seeds.',
                'id': 4,
                'time': '09:01:00'}
            ],
            response_json)

    def test_that_filter_between_times_works(self):
        self.client.force_authenticate(self.superuser)

        http_status, response_json = self._get(
                '/users/user_1/meals/?from_time=11:30&to_time=15:00')
        assert_equal(2, len(response_json))
        assert_equal([
            {
                'calories': 350,
                'date': '2015-01-01',
                'description': 'Poached eggs on toast.',
                'id': 2,
                'time': '13:00:00'},
            {
                'calories': 400,
                'date': '2015-01-02',
                'description': 'Prawn salad.',
                'id': 5,
                'time': '13:01:00'}
        ],
            response_json)
