all: deps lint test

deps:
	@python3 -m pip install --upgrade pip && pip3 install -r requirements-dev.txt

black:
	@black --line-length 120 pytest_service tests

isort:
	@isort --line-length 120 --use-parentheses --multi-line 3 --combine-as --trailing-comma pytest_service tests

flake8:
	@flake8 --max-line-length 120 --ignore C901,C812,E203,E704 --extend-ignore W503 pytest_service tests

pyright:
	@pyright pytest_service tests

lint: black isort flake8 pyright

test:
	@python3 -m pytest -vv --rootdir tests .

pyenv:
	echo pytest_service > .python-version && pyenv install -s 3.11.1 && pyenv virtualenv -f 3.11.1 pytest_service

pyenv-delete:
	pyenv virtualenv-delete -f pytest_service
