.PHONY: all

version_file := bootstrap4/_version.py
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
	isort -rc bootstrap4
	isort -rc demo
	isort -rc tests
	isort -rc *.py
	autoflake -ir *.py bootstrap4 demo tests --remove-all-unused-imports
	black .
	flake8 bootstrap4 demo tests *.py

publish: clean
	cd docs && make html
	python setup.py sdist
	twine upload dist/*
	git tag -a v$(version) -m 'tagging v$(version)'
