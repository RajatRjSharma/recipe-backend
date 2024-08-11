# Recipe API

## docker build -t recipe-api:v1.0.0

## docker run -d -p 8000:8000 --name recipe-api-v1.0.0 recipe-api:v1.0.0

## coverage run manage.py test

## coverage report

## docker compose up

## celery -A config beat -l info

## celery -A config worker -l info (linux)

## celery -A config worker -l info -P gevent (windows)
