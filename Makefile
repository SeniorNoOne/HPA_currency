manage_py := python app/manage.py

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt --upgrade

run:
	$(manage_py) runserver

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

flake8:
	flake8 app/

createsuperuser:
	$(manage_py) createsuperuser

worker:
	cd app && celery -A settings worker -l info --autoscale=0,2

schedule_worker:
	cd app && celery -A settings worker -Q scheduled_tasks -l info --autoscale=0,3

beat:
	cd app && celery -A settings beat -l info

test_data:
	$(manage_py) create_test_data

rm_test_data:
	$(manage_py) delete_test_data

pytest:
	pytest ./app/tests --cov=app --cov-report html && coverage report --fail-under=80

gunicorn:
	cd ./app && gunicorn --workers 4 --threads 4 settings.wsgi --timeout 36000 --max-requests 10000 -b localhost:8000
