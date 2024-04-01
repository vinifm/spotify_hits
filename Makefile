ENV_NAME = spot_venv

venv:
	python3 -m venv $(ENV_NAME)

install:
	pip install -r requirements.txt
