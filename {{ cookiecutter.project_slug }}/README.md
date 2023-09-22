# {{ cookiecutter.project_name }}

## Getting started

Copy .env-EXAMPLE to .env

Change .env if needed

Install the requirements:

    pipenv install

Create database

    pipenv run manage migrate

Create initial user

    pipenv run manage createsuperuser

Run the development server:

    pipenv run server

Go to http://localhost:8000/ in your browser
