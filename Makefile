.PHONY: venv install run

venv:
	python3 -m venv venv

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload