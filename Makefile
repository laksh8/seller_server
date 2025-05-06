.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: super-user
super-user:
	python manage.py createsuperuser

.PHONY: run-server
run-server:
	python manage.py runserver 8080

update: install migrate ;