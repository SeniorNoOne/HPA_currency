run:
	python app/manage.py runserver

showmigrations:
	python app/manage.py showmigrations

migrate:
	python app/manage.py migrate

flake8:
	flake8 app/
