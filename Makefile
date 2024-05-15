.ONESHELL:

SHELL := /bin/bash


# this is our root dir, this makefile must stay at the root of the repo
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP_NAME:="pp-dnp-stats"
VENV_NAME:=".venv"

.PHONY:
	run sync-deps setup-env bootstrap

setup-env:
	uv venv ${VENV_NAME}

venv:
	source ${VENV_NAME}/bin/activate

update-deps:
	uv pip compile -o requirements.txt requirements.in
	uv pip compile -o requirements-dev.txt requirements-dev.in

sync-deps:
	source ${VENV_NAME}/bin/activate
	uv pip sync requirements-dev.txt requirements.txt

bootstrap: | setup-env sync-deps

run:
	source ${VENV_NAME}/bin/activate
	${VENV_NAME}/bin/python -m streamlit run src/main.py
