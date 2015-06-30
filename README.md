# Calorie Counter Demo Application

This is a project demonstrating a simple static React JS frontend communicating
with a RESTful API built with Django Rest Framework.

## Run the backend (API)

The backend is written in Django 1.8.

### Install

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_for_tests.txt
```

### Run API tests

```
make test
```

The API tests live in the `apps/meals/tests/` directory.

### Migrate your database

For simplicity we use a sqlite3 database called `db.sqlite3`. First you'll want
to create an empty database:

```
make migrate_database
```

### Run the development webserver

By default the frontend expects to find the API running at `127.0.0.1:8000`

```
./manage.py runserver 0.0.0.0:8000
```

For convenience, you can now visit the API in your web browser at
[http://localhost:8000](http://localhost:8000)

## Run the frontend

The frontend is an HTML5 static site and lives in the `frontend/` directory.

You can serve this with Python's builtin webserver:

```
cd frontend
python2 -m SimpleHTTPServer 4000
```

Or on Python 3:

```
cd frontend
python3 -m http.server 4000
```

Now you can access the frontend by visiting [http://localhost:4000](http://localhost:4000)


## Play with the API

### Optional: Load demo fixtures

For convenience, you can load some example data which will make the following
users:

- `alice` with password `alice`
- `bob` with password `bob`
- `admin` with password `admin` (superuser)

And some meals belonging to `bob`.

```
make load_fixtures
```

There are two roles in the backend: normal users and "superusers". Superusers
are able to add, edit and delete other users' meals as well as users
themselves.

Normal users can only access their own meals.

### Get an API token

```
curl -X POST http://localhost:8000/api-token-auth/ -d '{"username": "alice", "password": "alice"}' -H 'Content-Type: application/json'
```

For convenience, you can store this in your environment:

```
export API_TOKEN=...
```

### Create a User

```
curl -X POST http://localhost:8000/users/ -d '{"username": "test_001", "password": "password_001"}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${API_TOKEN}"
```

### Retrieve a User

```
curl http://localhost:8000/users/test_001/ -H 'Content-Type: application/json' -H "Authorization: Bearer ${API_TOKEN}"
```

### Update a user

```
curl -X PUT http://localhost:8000/users/test_001/ -d '{"username": "test_001", "expected_daily_calories": 1000}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${API_TOKEN}"
```

### Delete a User

```
curl -X DELETE http://localhost:8000/users/test_001/ -H 'Content-Type: application/json' -H "Authorization: Bearer ${API_TOKEN}"
```

## Original Requirements

- User must be able to create an account and log in
- When logged in, user can see a list of his meals and calories (user enters
  calories manually, no auto calculations!), also he should be able to edit and
  delete
- Implement at least two roles with different permission levels (ie: a regular
  user would only be able to CRUD on his owned records, a user manager would be
  able to CRUD users, an admin would be able to CRUD on all records and users,
  etc.)
- Each entry has a date, time, text, and num of calories
- Filter by dates from-to, time from-to (e.g. how much calories have I had for
  lunch each day in the last month, if lunch is between 12 and 15h)
- User setting – Expected number of calories per day
- When displayed, it goes green if the total for that day is less than expected
  number of calories per day, otherwise goes red
- Minimal UI/UX design is needed.
- All actions need to be done client side using AJAX, refreshing the page is
  not acceptable. (If a mobile app, disregard this)
- REST API. Make it possible to perform all user actions via the API, including
  authentication (If a mobile application and you don’t know how to create your
  own backend you can use Parse.com, Firebase.com or similar services to create
  the API).
- In any case you should be able to explain how a REST API works and
  demonstrate that by creating functional tests that use the REST Layer
  directly.
- NOTE: Please keep in mind that this is the project that will be
  used to evaluate your skills. The project will be evaluated as if you are
  delivering it to a customer. We expect you to make sure that the app is fully
  functional and doesn’t have any obvious missing pieces.
