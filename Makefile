.PHONY: all

version_file := src/bootstrap4/_version.py
version := $(word 3, $(shell cat ${version_file}))

version:
	@echo $(version)

clean:
	rm -rf build dist *.egg-info

test:
	python manage.py test

tox:
	rm -rf .tox
	tox

reformat:
	isort -rc src/bootstrap4
	isort -rc example
	isort -rc tests
	isort -rc *.py
	autoflake -ir *.py src/bootstrap4 example tests --remove-all-unused-imports
	black .
	flake8 bootstrap4 example tests *.py

publish: clean
	cd docs && make html
	python setup.py sdist
	twine upload dist/*
	git tag -a v$(version) -m 'tagging v$(version)'
