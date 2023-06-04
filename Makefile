manage_py := python app/manage.py
docker_backend := docker-compose -f docker/docker-compose-dev.yml exec -it backend
docker_backend_python := docker-compose -f docker/docker-compose-dev.yml exec -it backend python app/manage.py

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt --upgrade

run:
	$(manage_py) runserver

run_d:
	$(docker_backend_python) runserver

showmigrations:
	$(manage_py) showmigrations

showmigrations_d:
	$(docker_backend_python) showmigrations

init_db:
	$(manage_py) makemigrations
	$(manage_py) migrate

init_db_d:
	$(docker_backend_python) makemigrations
	$(docker_backend_python) migrate

makemigrations:
	$(manage_py) makemigrations

makemigrations_d:
	$(docker_backend_python) makemigrations

migrate:
	$(manage_py) migrate

migrate_d:
	$(docker_backend_python) migrate

shell:
	$(manage_py) shell_plus --print-sql

shell_d:
	$(docker_backend_python) shell_plus --print-sql

flake8:
	flake8 app/

flake8_d:
	$(docker_backend) flake8 app/

createsuperuser:
	$(manage_py) createsuperuser

createsuperuser_d:
	$(docker_backend_python) createsuperuser

celery_worker:
	cd app && celery -A settings worker -l info --autoscale=0,2

celery_schedule_worker:
	cd app && celery -A settings worker -Q scheduled_tasks -l info --autoscale=0,3

celery_beat:
	cd app && celery -A settings beat -l info

test_data:
	$(manage_py) create_test_data

test_data_d:
	$(docker_backend_python) create_test_data

rm_test_data:
	$(manage_py) delete_test_data

rm_test_data_d:
	$(docker_backend_python) delete_test_data

pytest:
	pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=80

pytest_d:
	$(docker_backend) pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=80

gunicorn:
	cd ./app && gunicorn --workers 4 --threads 4 settings.wsgi --timeout 36000 --max-requests 10000 -b localhost:8000

collectstatic:
	$(manage_py) collectstatic --no-input

collectstatic_d:
	$(docker_backend_python) collectstatic --no-input

terminal_d:
	docker-compose -f docker/docker-compose-dev.yml exec -it backend bash
