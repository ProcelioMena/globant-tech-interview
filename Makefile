# project variables
APP_CONT ?= globant-api

# Aesthetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "WARNING: $$1"; printf $(NC)' MESSAGE

.PHONY: unit-test lint dev stop install

install:
	${INFO} "Installing requirements for globant-tech-interview"
	@ pip3 install -r requirements.txt

lint:
	${INFO} "Running Flake8 on all files"
	@ flake8 --config setup.cfg

stop:
	${INFO} "Resetting containers..."
	if docker ps -a --format '{{.Names}}' | grep -q $(APP_CONT); then\
		docker stop $(APP_CONT); \
		docker rm $(APP_CONT); \
	fi

dev: stop
	${INFO} "Spinning up  API locally..."
	python3 src/app.py
#	@ docker-compose $(COMPOSE_FILE) build
	#@ docker-compose $(COMPOSE_FILE) up
