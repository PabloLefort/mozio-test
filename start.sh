#!/bin/sh

sh ./wait-for-it.sh

python3.9 manage.py migrate
python3.9 manage.py runserver 0.0.0.0:8000