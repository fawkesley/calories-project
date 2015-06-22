.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	find . -iname __pycache__ -type d -delete

.PHONY: test
test:
	./manage.py test -v 3 --failfast

.PHONY: nuke_database
nuke_database:
	rm -f db.sqlite3

.PHONY: migrate_database
migrate_database:
	./manage.py migrate

.PHONY: load_fixtures
load_fixtures: migrate_database fixtures/demo.json
	./manage.py loaddata fixtures/demo.json

.PHONY: fresh
fresh: nuke_database load_fixtures
