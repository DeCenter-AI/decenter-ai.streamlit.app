setup:
	# pip install pre-commit
	# pre-commit install
	# python -m venv venv
	# source venv/bin/activate
	@make install
	pre-commit autoupdate

activate:
	source $(poetry env info --path)/bin/activate

install:
	# @ pip install --upgrade pip
	# @ pip install -r requirements.txt
	@pip install poetry
	@poetry install --no-root


run:
  # @source venv/bin/activate
	@venv/bin/python -m streamlit run main.py

install-tests:
	# @python -m pip install -r requirements-test.txt
	@make install

test:
	@pytest -p no:cacheprovider
	@echo "testing complete"

clean:
	@echo "cleaning"
	@find . -type d -name '.pytest_cache' -exec rm -rf {} +
	@find . -type d -name 'testcache' -exec rm -rf {} +
	@find . -type d -name '.benchmarks' -exec rm -rf {} +
	@find . -type f -name '<_io.BytesIO object at*' -exec rm -f {} +
	@find . -type f -name '*.log' -exec rm -f {} +

docker:
	docker build -t review-ai .

.PHONY: run install clean setup test

poetry-export:
	poetry export --with dev --format requirements.txt --output requirements.txt
