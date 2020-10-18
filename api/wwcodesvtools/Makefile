.PHONY: help translate test clean update compass collect rebuild

SETTINGS={{ project_name }}.settings
TEST_SETTINGS={{ project_name }}.test_settings

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# migrate: migrate - runs new migrations on your db
migrate:
	python manage.py migrate

# target: test - calls the "test" django command
test:
	python manage.py test

# target: setup - sets up your repository and project
setup:
	pip install pre-commit
	pre-commit install
