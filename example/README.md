# Example project for django-bootstrap4

This example project only supports the latest version of Django.

## Instructions

To run the example:

```bash
git clone https://github.com/zostera/django-bootstrap4.git

cd django-bootstrap4/example
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
or using docker:
```bash
git clone https://github.com/zostera/django-bootstrap4.git

cd django-bootstrap4/example
docker compose build
docker compose run example python manage.py migrate
docker compose up
```

Server should be live at http://127.0.0.1:8000/ now.
