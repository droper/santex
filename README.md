# Python/Django Challenge

## Description
Python/Django implementation of the Santex challenge.

## How to run the project
* Create a virtualenv: `python -m venv virtualenv` and activate it `source virtualenv/bin/activate`.
* Install dependencies: `pip install -r requirements.txt`
* Create the initial migration: `python manage.py makemigrations`
* Execute the api service admin migrations: `python manage.py migrate`
* Start the api service: `cd api_service ; ./manage.py runserver 8000`

## Create two users
* Create a superuser: `python manage.py createsuperuser`
* Login into `http://127.0.0.1:8000/admin` and create a normal user.

