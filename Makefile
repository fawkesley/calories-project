.PHONY: clean
clean:
	find . -iname '*.pyc' -delete
	find . -iname __pycache__ -type d -delete

.PHONY: test
test:
	./manage.py test -v 3 --failfast
