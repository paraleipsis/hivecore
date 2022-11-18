#!/bin/sh

cd api && python3 manage.py runserver 0.0.0.0:7001 &

cd api && celery -A liquorice worker --loglevel=info &

cd api && celery -A liquorice beat --loglevel=info &

cd frontend && serve -s build -l 3000  
