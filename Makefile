.PHONY: help test coverage pre-commit monitor mpremote circup-list circup-update docs deploy lint

help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'
	@echo
	@echo "run make target ARGS=args... to pass arbitrary arguments to a target."
	@echo "example: make circup ARGS=freeze"

test: ## run unit tests
	uv tool run --with pytest-cov pytest ${ARGS}

coverage: ## run unit tests and create HTML coverage report
	uv tool run --with pytest-cov pytest --cov-report html:cov_html
	echo "run 'xdg-open cov_html/index.html' to view the report."

pre-commit: ## run pre-commit hook
	 uv tool run --from pre-commit pre-commit run --all-files

mpremote: ## run mpremote with arguments specified in ARGS
	uv tool run mpremote ${ARGS}

repl: ## run mpremote to create a remote REPL on the device
	uv tool run mpremote repl

circup: ## call circup with arbitrary arguments specified in ARGS, e.g. make circup ARGS=freeze
	uv tool run circup ${ARGS}

circup-update: ## update all packages on the device
	uv tool run circup update --all

docs:  ## build docs
	cd docs && uv tool run --python 3.13 --with sphinx_rtd_theme --from sphinx sphinx-build -E -W -b html . _build/html

deploy: ## copy local files to the device
	echo TODO

lint: ## run ruff linter
	uv tool run ruff check .
