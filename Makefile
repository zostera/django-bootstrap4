.PHONY: all

clean:
	rm -rf build dist *.egg-info

test:
	python manage.py test

tox:
	rm -rf .tox
	tox

reformat:
	isort -rc bootstrap4
	isort -rc demo
	autoflake -ir bootstrap4 demo tests --remove-all-unused-imports
	black .
	flake8 bootstrap4 demo tests

publish: clean
	cd docs && make html
	python setup.py sdist
	twine upload dist/*
