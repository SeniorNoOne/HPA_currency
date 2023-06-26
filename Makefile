manage_py := python app/manage.py
docker_dev := docker-compose -f docker/docker-compose-dev.yml
docker_backend := docker-compose -f docker/docker-compose-dev.yml exec -it backend
docker_backend_python := docker-compose -f docker/docker-compose-dev.yml exec -it backend python app/manage.py

# venv commands
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt --upgrade

showmigrations:
	$(manage_py) showmigrations

init_db:
	$(manage_py) makemigrations
	$(manage_py) migrate

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

createsuperuser:
	$(manage_py) createsuperuser

flake8:
	flake8 app/

pytest:
	pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=85

celery_worker:
	cd app && celery -A settings worker -l info --autoscale=0,2 --pool threads

celery_schedule_worker:
	cd app && celery -A settings worker -Q scheduled_tasks -l info --autoscale=0,3

celery_beat:
	cd app && celery -A settings beat -l info

test_data:
	$(manage_py) create_test_data

rm_test_data:
	$(manage_py) delete_test_data

collectstatic:
	$(manage_py) collectstatic --no-input

gunicorn:
	cd ./app && gunicorn --workers 4 --threads 4 settings.wsgi --timeout 36000 --max-requests 10000 -b localhost:8000

run:
	$(manage_py) runserver

# Docker commands
showmigrations_d:
	$(docker_backend_python) showmigrations

init_db_d:
	$(docker_backend_python) makemigrations
	$(docker_backend_python) migrate

makemigrations_d:
	$(docker_backend_python) makemigrations

migrate_d:
	$(docker_backend_python) migrate

shell_d:
	$(docker_backend_python) shell_plus --print-sql

createsuperuser_d:
	$(docker_backend_python) createsuperuser

flake8_d:
	$(docker_backend) flake8 app/

pytest_d:
	$(docker_backend) pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=85

test_data_d:
	$(docker_backend_python) create_test_data

rm_test_data_d:
	$(docker_backend_python) delete_test_data

collectstatic_d:
	$(docker_backend_python) collectstatic --no-input

run_d:
	$(docker_backend_python) runserver

terminal_d:
	$(docker_dev) exec -it backend bash

build_d:
	$(docker_dev) build

up_d:
	$(docker_dev) up -d

up_build_d:
	$(docker_dev) up -d --build

restart_d:
	$(docker_dev) restart

stop_d:
	$(docker_dev) stop

down_d:
	$(docker_dev) down
