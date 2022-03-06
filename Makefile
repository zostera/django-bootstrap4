.PHONY: test tox reformat lint docs porcelain branch build publish example

PROJECT_DIR=src/django_bootstrap4
PYTHON_SOURCES=${PROJECT_DIR} tests example *.py

example:
	cd example && python manage.py runserver

test:
	coverage run manage.py test
	coverage report

tox:
	rm -rf .tox
	tox

reformat:
	autoflake -ir --remove-all-unused-imports ${PYTHON_SOURCES}
	isort ${PYTHON_SOURCES}
	docformatter -ir --pre-summary-newline --wrap-summaries=0 --wrap-descriptions=0 ${PYTHON_SOURCES}
	black .

lint:
	flake8 ${PYTHON_SOURCES}
	pydocstyle --add-ignore=D1,D202,D301,D413 ${PYTHON_SOURCES}

docs:
	rm -rf docs/_build
	cd docs && sphinx-build -b html -d _build/doctrees . _build/html

porcelain:
ifeq ($(shell git status --porcelain),)
	@echo "Working directory is clean."
else
	@echo "Error - working directory is dirty. Commit those changes!";
	@exit 1;
endif

branch:
ifeq ($(shell git rev-parse --abbrev-ref HEAD),main)
	@echo "On branch main."
else
	@echo "Error - Not on branch main!"
	@exit 1;
endif

build: docs
	rm -rf build
	rm -rf dist
	python setup.py sdist bdist_wheel

publish: porcelain branch build
	twine upload dist/*
	rm -rf dist
