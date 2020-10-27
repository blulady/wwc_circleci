.PHONY: help translate test clean update compass collect rebuild

SETTINGS={{ project_name }}.settings
TEST_SETTINGS={{ project_name }}.test_settings

# colors
RED='\033[0;31m'
NC='\033[0m' # no color

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME)!"
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

# target: setup_repo - sets up your local repository and project
setup_repo:
	@echo "${RED}NOTE This can only be run in your local environment, do not attempt to run this in the docker container."
	@echo
	@echo "${RED}NOTE This needs python3 as your default python version and pip3 as your default pip."
	@echo
	pip install pre-commit
	pre-commit install
