# Django Pet Project

This is a pet project built using Django, featuring various implemented features and technologies. 
It serves as a showcase of Django best practices and commonly used tools in Django development.

Table of Contents
- [Configuration Modes](#configuration-modes)
- [Installation](#installation)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Additional Notes](#additional-notes)


## Configuration Modes

This project offers flexible configuration options and can be used in different modes. 
Choose the appropriate one based on your requirements and follow the corresponding 
instructions for setup and deployment.

Also notice that the project offers `Makefile` commands that simplify work with it, so it's highly 
recommended to install [Makefile](https://www.gnu.org/software/make/). 

Please note that for each configuration mode, specific steps and configurations may be necessary. 
Refer to the relevant sections in the documentation or README for detailed instructions on how to 
configure and run the project in each mode.

### **Simplified Venv Mode** 
In this mode, the project utilizes development settings. The WSGI server and RabbitMQ are used as 
the broker. Any Django compatible DB can be used if properly configured, but this project supposes 
that SQLite3 or Postgres is used. This mode is suitable for local development and testing. 
List of required software:
- [RabbitMQ](https://www.rabbitmq.com/#getstarted)
- [PostgreSQL](https://www.postgresql.org/download/) (optional if used remote DB connection) - or other preferable Django 
compatible DB engine in case of development with local DB engine
- [PgBouncer](https://www.pgbouncer.org/install.html) (optional) - required for Postgres connection polling

### **Venv Mode**
In this mode, the project employs production settings, including Nginx, Gunicorn, PostgreSQL, and 
RabbitMQ. This setup is recommended for deploying the project to a production  environment. 
List of required software:
- [Nginx](https://nginx.org/en/download.html)
- [RabbitMQ](https://www.rabbitmq.com/#getstarted)
- [PostgreSQL](https://www.postgresql.org/download/) (optional if used remote DB connection) - or other preferable Django 
compatible DB engine in case of development with local DB engine
- [PgBouncer](https://www.pgbouncer.org/install.html) (optional) - required for Postgres connection polling


### **Containerized Mode** 
The project also supports a containerized production mode. This mode allows to deploy the project 
using containerization technologies such as Docker. It provides an isolated and reproducible 
environment for running the project in a production setting. In this mode such technologies are 
used Nginx, Gunicorn, PostgreSQL, and RabbitMQ. List of required software:
- [Docker Engine](https://docs.docker.com/engine/install/)

## Installation

After installation all the necessary software for a preferable configuration mode, let's go further 
to installation. This section consist of installation guide for Venv (both of them) and 
Containerized modes.

### Installation for **Venv Modes**

1. Copy the repo: `git clone https://github.com/SeniorNoOne/HPA_currency.git`
2. Create virtual environment inside of root of the project: `python -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install the required dependencies: `pip install -r requirements.txt`
5. Apply DB migration using provided `makefile` command: `make migrate` or using directly command
`python app/manage.py migrate`
6. Collect static files using `makefile` command: `make collectstatic` or using command 
`python app/manage.py collectstatic`
7. Launch server using `makefile` command: `make run` or `python app/manage.py run`

### Installation for **Containerized Mode**

1. Launch **Docker Engine**
2. Build backend image from Dockerfile using `Makefile` command `make build` or 
`docker-compose -f docker/docker-compose-dev.yml build`
3. Run docker-compose images using `make up_d` or `docker-compose -f docker/docker-compose-dev.yml up -d`
4. After this step to ensure that images are built correct visit [localhost](http://127.0.0.1:80). 
Error message with 500 code means that images are built correct, but DB migrations were not applied
5. To apply DB migrations using `make migrate_d` or`docker-compose -f docker/docker-compose-dev.yml 
exec -it backend migrate` 
6. Collect static files `make collectstatic_D` or`docker-compose -f docker/docker-compose-dev.yml 
exec -it backend collectstatic` 
7. At this point everything should work fine, but to ensure restart containers using `make restart_d`
or `docker-compose -f docker/docker-compose-dev.yml restart`


## Features
The Django pet project offers various features and functionalities that can be explored once the 
project is set up and running. Here are some of the main features:
- **User Registration and Authentication**. Users can sign up and log in to the application, 
allowing them to access personalized features and data.
- **Currency Source and Rate Management**. The project allows users to create currency sources 
and their corresponding rates using the Source and Rate models.
- **Feedback Submission**. Users can submit feedback through the application, which is sent to a 
moderator using a third-party SMTP service for further review.
- **Rate Parsing**. The project implements rate parsing functionality using BeautifulSoup4 for 
web scraping and interacting with third-party APIs.
- **Caching with Memcached**. To optimize performance and reduce database load, the project utilizes
Memcached, an in-memory caching system.
- **Nginx and Gunicorn**. Nginx serves as the web server, while Gunicorn acts as the WSGI server 
for running the Django application, ensuring efficient handling of HTTP requests.
- **Django Signals**. The project utilizes Django Signals to implement decoupled and reusable 
event-driven architecture, enabling various actions to be triggered based on specific signals.
- **Logging**. Middleware and a separate model are employed for logging purposes, allowing for 
effective tracking and analysis of application events.
- **Admin Interface**. Django's built-in admin interface is available for managing the 
application's data, providing an intuitive and user-friendly interface for administrators.
- **Bootstrap**. The project uses the Bootstrap framework for creating responsive and visually 
appealing user interfaces, ensuring a modern and engaging user experience.
- **Database Support**. The project supports both SQLite3 for development purposes and Postgres 
for production deployment, providing flexibility and scalability in data storage.
- **Docker and Docker Compose**. Docker and Docker Compose are utilized for containerization, 
simplifying deployment and management of the project in different environments.
- **Code Quality and Testing**. Flake8 is used as a linting tool to enforce Python code style and 
best practices, while Django-pytest enables comprehensive testing of the application's functionality.
- **REST API with Django Rest Framework (DRF)**. The project implements a REST API using Django 
Rest Framework, allowing for seamless integration with external systems and enabling data exchange 
in a structured manner.
- **Custom Bootstrap Forms for django-filter.** The project incorporates custom Bootstrap forms that are 
integrated with django-filters. These forms, created using FormHelper, provide a seamless and user-friendly filtering 
experience, enhancing the overall usability of the application.

## Technologies Used
The Django pet project incorporates the following technologies:

- **Django**. A Python web framework used for building powerful and scalable web applications.
- **Python**. The programming language used for the project's backend development.
- **SQLite3** A lightweight and file-based database used for local development and testing purposes.
- **PostgreSQL**. A production-grade relational database management system, providing a robust 
and scalable data storage solution.
- **Docker**. A platform for containerization and automated deployment of applications, ensuring 
consistency and reproducibility.
- **Docker Compose**. A tool for defining and running multi-container Docker applications, 
simplifying the deployment and management process.
- **Nginx**. A high-performance web server used for handling HTTP requests and serving static 
files efficiently.
- **Gunicorn**. A Python WSGI HTTP server commonly used for running Django applications in 
production environments.
- **BeautifulSoup4**. A library for web scraping and parsing HTML/XML documents, used for rate 
parsing functionality.
- **Memcached**. An in-memory caching system used to optimize performance and reduce database load.
- **Bootstrap**. A popular CSS framework utilized for creating responsive and modern user interfaces.
- **RabbitMQ**. A messaging broker used for reliable communication between components, particularly 
for handling feedback submissions and email sending.
- **SMTP Service**. A third-party SMTP (Simple Mail Transfer Protocol) service integrated into 
the project for sending emails.
- **Django Signals**. A feature of Django used for implementing decoupled and reusable 
event-driven architecture.
- **Flake8**. A linting tool used for enforcing Python code style and best practices.
- **Django-pytest**. A testing framework used for comprehensive testing of the application's 
functionality.
- **Django Rest Framework (DRF)**. A powerful toolkit for building RESTful APIs, enabling seamless 
integration with external systems.
- **Django-filters.** A versatile filtering library for Django applications, enabling the implementation of 
complex query filters and search functionality. It integrates seamlessly with Django models and provides a 
convenient way to handle filtering logic.

These technologies collectively contribute to the functionality, performance, security, 
and maintainability of the project.


## Additional Notes

- Local settings and env sample files are provided. 
- Notice that static files are properly served only if `DEBUG = True` which is the case for base and
local sample setting files. Be aware of using `DEBUG = True` in production.
- In `docker-compose-dev.yml` Postgres DB image is created. It's done only for dev purpose.
- Note that settings in config files for nginx, PgBouncer and other third party software used in this project must 
match Django settings in `local.py` file.
- For such third party software basic config files are provided in the project's root directory.
