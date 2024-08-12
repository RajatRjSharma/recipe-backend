# Recipe API

- ### Before starting further please create a python environment first, then install requirements.txt and add a .env with required envs as shown in .env.example

  ```
  (Add python env)
  python -m venv <envname>

  (Activate python env)
  ./env/bin/activate  (linux)
  .\env\Scripts\activate   (windows)

  (Deactivate)
  deactivate

  (Install all required packages in python env)
  pip install -r requirements.txt

  (Add .env with required envs from .env.example file)

  (Please check output folder for email and coverage images)
  ```

- ### Docker integration

- Added Dockerfile for django project
- Docker compose for containerizing django project and redis for celery

  ```
  (Build Docker Image)
  docker build -t recipe-api:v1.0.0

  (Run Docker Image will also take env mentioned in .env.example file -e env value)
  docker run -d -p 8000:8000 --name recipe-api-v1.0.0 recipe-api:v1.0.0

  (Recommended all in one step, will used config defined in docker-compose.yml file, also requires .env with all env mentioned in .env.example file)
  docker compose up (Windows)
  docker-compose up (Linux)
  ```

- ### Testing and Coverage report

- Added the testcases for both user and recipe module in a respective test.py file.
- Also ran the coverage report, I have added screen shot in output folder in root.

  ```
  (Run all test cases)
  python manage.py test

  (Run test cases with coverage report)
  coverage run manage.py test

  (View coverage report)
  coverage report/html/xml
  ```

- ### Asynchronous Task Handling with Celery

- Integrated Celery by adding its config in base.py and creating respective celery.py in config for its instantiation, task scan.
- Also integrated Redis which act as broker and backup db for celery. Updated it in docker compose to containerized with project when docker compose is run.

  ```
  (Watch on celery tasks invoke and status on completion)
  celery -A config worker -l info (linux)
  celery -A config worker -l info -P gevent (windows)
  ```

- ### Email Queue Implementation

- Added a daily email notification on the like received on their recipes.
- Used celery beat to get it done, Added a task for same in users/tasks.py and added a beat schedule for it in config/celery.py file which will invoke mid night at 00:00 UTC.

  ```
  (Watch on celery bead tasks invoke)
  celery -A config beat -l info
  ```

- ### Logging Framework

- Added the config for logger in base.py for info, debug, error and format.
- Also integrated it in recipe/view.py

- ### Update the code to github

  [Github Repo](https://github.com/RajatRjSharma/recipe-backend)

- ### Added a AWS EC2 instance, Postgres DB, Nginx, Docker configured (You may get warning for ssl certificate but you can accept it as I have used openssl for demonstration)

  [Live version](https://ec2-13-127-195-54.ap-south-1.compute.amazonaws.com/)
