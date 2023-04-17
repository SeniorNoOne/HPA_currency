manage_py := python app/manage.py

install:
	pip install -r requirements.txt

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

mail_worker:
	cd app && celery -A settings worker -Q mail -l info --autoscale=0,2

storage_worker:
	cd app && celery -A settings worker -Q storage_tasks -l info --autoscale=0,2

schedule_worker:
	cd app && celery -A settings worker -Q scheduled_tasks -l info --autoscale=0,3

beat:
	cd app && celery -A settings beat -l info
