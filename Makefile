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

shell:
	$(manage_py) shell_plus --print-sql

flake8:
	flake8 app/

createsuperuser:
	$(manage_py) createsuperuser
