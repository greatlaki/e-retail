.PHONY: install
install:
	$(call log, installing packages)
	poetry install

.PHONY: format
format:
	$(call log, reorganizing imports & formatting code)
	poetry run black .
	poetry run ruff . --fix --exit-zero
	poetry run pre-commit run --all
	poetry run mypy .

.PHONY: lint
lint:
	poetry run ruff . --fix --exit-zero

.PHONY: test
test:
	poetry run coverage run -m pytest
	poetry run coverage report

.PHONY: run
run:
	poetry run python3 ./backend/manage.py runserver

.PHONY: init-data
run:
	$(call log, data initialization)
	./manage.py loaddata fixtures/initial_data.json
