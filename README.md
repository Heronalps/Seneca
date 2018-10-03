# Celery-Lambda

## User Guidance
- Direct to repo directory /Celery_Lambda, run ``` celery -A proj worker -l info ```
- In another terminal, run ``` python clean_up_logs.py /aws/lambda/container_tester ```
- In another Terminal, run ``` python run.py ``` with 3 arguments, celery_async, lambda_async, invoke_time
