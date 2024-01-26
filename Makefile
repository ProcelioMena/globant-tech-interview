# project variables
APP_CONT ?= globant-api

# Aesthetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "WARNING: $$1"; printf $(NC)' MESSAGE

.PHONY: unit-test int-test lint dev stop install

install:
	${INFO} "Installing requirements for globant-tech-interview"
	@ pip3 install -r requirements.txt
	@ pre-commit install

lint:
	${INFO} "Running Flake8 on all files"
	@ flake8 --config setup.cfg

unit-test:
	${INFO} "Running unit tests"
	pytest tests/unit/ 

stop:
	${INFO} "Resetting containers..."
	ifeq $ shell docker ps -a --format '{{.Names}}' | grep $(APP_CONT)
		docker stop $(APP_CONT)
		docker rm $(APP_CONT)
	endif

dev: stop
	${INFO} "Spinning up  API locally..."
	@ docker-compose $(COMPOSE_FILE) build
	@ docker-compose $(COMPOSE_FILE) up
