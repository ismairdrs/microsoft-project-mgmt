PROJECT_NAME = microsoft
TEST_FOLDER = tests
APPLICATION = microsoft.api.main:app


.PHONY: typecheck
typecheck:
	mypy --python-version 3.11 --ignore-missing-imports --disallow-untyped-defs --disallow-untyped-calls $(PROJECT_NAME)/


.PHONY: format
format:
	@echo ""
	@echo "FORMATTING CODE:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview $(PROJECT_NAME) $(TEST_FOLDER)
	unify --in-place --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)
	isort --profile black .

	@echo ""
	@echo "CHECKING CODE STILL NEEDS FORMATTING:"
	@echo ""
	black -l 88 -t py310 --skip-string-normalization --preview --check $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "CHECKING TYPING"
	@echo ""
	@make typecheck

	@echo ""
	@echo "CHECKING CODE STYLE"
	@echo ""
	flake8 $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "ENSURE DOUBLE QUOTES"
	@echo ""
	unify --check-only --recursive --quote '"' $(PROJECT_NAME) $(TEST_FOLDER)

	@echo ""
	@echo "SORT IMPORTS"
	@echo ""
	isort --profile black -c .

	@echo ""
	@echo "CHECKING SECURITY ISSUES"
	@echo ""
	bandit -r $(PROJECT_NAME)

.PHONY: clean
clean:
	- @find . -name "*.pyc" -exec rm -rf {} \;
	- @find . -name "__pycache__" -delete
	- @find . -name "*.pytest_cache" -exec rm -rf {} \;
	- @find . -name "*.mypy_cache" -exec rm -rf {} \;

.PHONY: db_upgrade
db_upgrade:
	alembic upgrade head

.PHONY: db_generate_revision
db_generate_revision:
	alembic revision --autogenerate

.PHONY: run
run:
	uvicorn $(APPLICATION) --reload


.PHONY: db_upgrade_test
db_upgrade_test:
	DB_PORT=5435 DB_USER=postgres DB_PASS=microsoft_test DB_HOST=127.0.0.1 DB_PORT=5435 DB_NAME=microsoft_test DB_POOL_SIZE=5 DB_MAX_OVERFLOW=0 alembic upgrade head


.PHONY: unit-test
unit-test:
	pytest tests/unit/ -vv

.PHONY: integration-test
integration-test:
	-	docker container stop microsoft_test_db
	-	docker container rm microsoft_test_db
	docker run -d --name microsoft_test_db -e "POSTGRES_DB=microsoft_test" -e "POSTGRES_PASSWORD=microsoft_test" -P -p 127.0.0.1:5435:5432 postgres:14-alpine
	sleep 3
	-  @make db_upgrade_test
	pytest tests/integration/ -vv
	docker container stop microsoft_test_db
	docker container rm microsoft_test_db


.PHONY: coverage
coverage:
	coverage run -m pytest tests/unit/ -vv
	coverage report -m
