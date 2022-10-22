#!/bin/bash
#  this script installs the requirements in a created virtual environment, runs the migrations and eventually runs the server

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver