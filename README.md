# Seneca
A framework of auto-packaging, deployment, optimization and hyperparameter-tuning for Serverless function

# User Guidance

## CLI Installation

* Install pipsi:
```
curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
```
* Install seneca:
```
cd <rootdir-of-Seneca>
pipsi install ./cli
```
* Usage
```
seneca --help
```

## Prerequisite
- Start Rabbitmq Server, run ``` sudo rabbitmq-server ```
- Start Redis Server, run ``` redis-server ```
- Direct to repo directory /Celery_Lambda, run ``` celery -A proj worker -l info ```

## Container-Test
- In another terminal at repo directory, run ``` python run_container_test.py ``` with 3 arguments, celery_async, lambda_async, invoke_time

## Centaurus 
- The aws branch is a hybrid solution, which needs a PostgreSQL server


## Prophet

* Install Prophet on masOS

Since gcc hookup issue, please install Pystan ```BEFORE``` installing fbprophet, and they ```CANNOT``` be in one pip install command.

```
pip install numpy==1.15.4
pip install pystan
pip install fbprophet
```
* Auto packaging and deployment to Lambda
```
cd ./src/lambda_func/prophet
docker-compose up
```