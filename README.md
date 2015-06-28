## Run Backend

Backend is written in Python / Django.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_for_tests.txt
```

## Test

```
make test
```

## Play with the API

### Migrate your database

```
make migrate_database
```


### Load demo fixtures

```
make load_fixtures
```

### First, make a superuser (admin)

```
./manage.py createsuperuser --username admin --email admin@admin.com
```

The following examples assume you set the password to "admin"...

### Get an API token

```
curl -X POST http://localhost:8000/api-token-auth/ -d '{"username": "bob", "password": "bobspassword"}' -H 'Content-Type: application/json'
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

## Requirements

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
