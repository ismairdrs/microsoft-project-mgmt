PROJECT_NAME = microsoft
TEST_FOLDER = tests
APPLICATION = microsoft.api.main:app


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
