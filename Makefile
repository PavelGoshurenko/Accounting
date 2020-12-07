# Makefile

install:
	poetry install
lint:
	poetry run flake8
test:
	poetry run coverage run --source='.' --omit '.venv/*' manage.py test
	poetry run coverage report
	poetry run coverage xml
	
run:
	poetry run python manage.py runserver

requirements:
	poetry export -f requirements.txt -o requirements.txt

migrate:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

