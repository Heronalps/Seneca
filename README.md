# User Guidance

## Prerequisite
- Start Rabbitmq Server, run ``` sudo rabbitmq-server ```
- Start Redis Server, run ``` redis-server ```
- Direct to repo directory /Celery_Lambda, run ``` celery -A proj worker -l info ```

## Container-Test
- In another terminal at repo directory, run ``` python run_container_test.py ``` with 3 arguments, celery_async, lambda_async, invoke_time

## Centaurus 
- The aws branch is a hybrid solution, which needs a PostgreSQL server

## N-Body
- 