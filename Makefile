# project variables
APP_CONT ?= globant-api

# Aesthetics
RED := "\e[1;31m"
YELLOW := "\e[1;33m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "=> $$1"; printf $(NC)' MESSAGE
WARNING := @bash -c 'printf $(RED); echo "WARNING: $$1"; printf $(NC)' MESSAGE

.PHONY: unit-test lint dev install

install:
	${INFO} "Installing requirements for globant-tech-interview"
	@ pip3 install -r requirements.txt

lint:
	${INFO} "Running Flake8 on all files"
	@ flake8 --config setup.cfg

unit-test:
	${INFO} "Running unit tests"
	@ pytest tests/unit/ -c pytest.ini

dev: stop
	${INFO} "Spinning up  API locally..."
	@ docker run -p 8080:8080 ${APP_CONT}
