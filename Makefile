# Makefile

install:
	poetry install
lint:
	poetry run flake8
	
run:
	poetry run python manage.py runserver

requirements:
	poetry export -f requirements.txt -o requirements.txt

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

heroku:
	git push heroku master
