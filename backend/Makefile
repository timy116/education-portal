.PHONY: all run app migrate

BASE_PATH := $(shell dirname $(shell pwd))
NAME ?= apps
APPS_DIR := $(BASE_PATH)/backend/apps
MANAGE := $(shell dirname $(APPS_DIR))/manage.py


all:
	@echo "Nothing to be done for 'make'."

run:
	python manage.py runserver --settings "backend.settings.dev"

app:
	@ cd $(APPS_DIR); \
	python $(MANAGE) startapp $(NAME);

migrate:
	python manage.py makemigrations --settings "backend.settings.dev"; \
	python manage.py migrate --settings "backend.settings.dev"; 
