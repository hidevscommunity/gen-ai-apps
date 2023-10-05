setup:
	pip install pre-commit
	pre-commit install
	python -m venv venv
	source venv/bin/activate

	pre-commit autoupdate

install:
	@ pip install --upgrade pip
	@ pip install -r requirements.txt

run:
	@python -m streamlit run app.py

install-tests:
	@ python -m pip install -r requirements-test.txt

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

.PHONY: run install clean setup test
