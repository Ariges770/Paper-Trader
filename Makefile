VENV = venv_paper_trader
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
SHELL := /bin/bash

all: venv


run:
	clear
	flask run

debug:
	clear
	flask --debug run

$(VENV)/bin/activate: requirements.txt
	clear
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


venv: $(VENV)/bin/activate


test: requirements.txt
	clear
	pytest


upload: requirements.txt
	vercel

prod: requirements.txt
	vercel --prod


clean:
	clear
	rm -rf __pycache__
	rm -rf .pytest_cache
	py3clean .
	rm -rf $(VENV)


version:
	$(PYTHON) --version

.PHONY: all run clean version
