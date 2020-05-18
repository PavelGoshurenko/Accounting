# Makefile

install:
	python3 -m poetry install
lint:
	python3 -m poetry run flake8
test:
	python3 -m poetry run coverage run --source='.' --omit '.venv/*' manage.py test
	python3 -m poetry run coverage report
	python3 -m poetry run coverage xml
	
run:
	python3 -m poetry run python manage.py runserver

requirements:
	python3 -m poetry export -f requirements.txt -o requirements.txt

migrate:
	python3 -m poetry run python3 manage.py makemigrations
	python3 -m poetry run python3 manage.py migrate

