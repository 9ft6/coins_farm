.PHONY: help install install-dev run tests

help: ## Show list of commands
	@printf "\033[33m%s:\033[0m\n\n" 'Available commands'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup_venv = test -d venv || python3.11 -m venv venv
pip_install = pip install -r requirements.txt
activate = . venv/bin/activate

install: ## Make venv
	$(setup_venv)
	$(activate) && $(pip_install)

install-dev: ## Make venv
	$(activate) && $(pip_install) -r requirements-dev.txt

run: ## Run app
	$(activate) && cd src && python app.py
