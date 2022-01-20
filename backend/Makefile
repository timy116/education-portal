.PHONY: all run app freeze install

BASE_PATH := $(shell dirname $(shell pwd))
NAME ?= apps
APPS_DIR := $(BASE_PATH)/backend/apps
MANAGE := $(shell dirname $(APPS_DIR))/manage.py


all:
	@echo "Nothingz to be done for 'make'."

run:
	python manage.py runserver --settings "backend.settings.dev"

app:
	cd $(APPS_DIR); \
	python $(MANAGE) startapp $(NAME);

freeze:
	@source "$(BASE_PATH)/venv/Scripts/activate"; \
	pip freeze;

install:
	@source "$(BASE_PATH)/venv/Scripts/activate"; \
	pip install $(NAME);
