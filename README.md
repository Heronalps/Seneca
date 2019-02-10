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

## Execution
- Start EC2 instance
- Start Rabbitmq Server, run ``` sudo rabbitmq-server ```
- Configure Rabbitmq,run ``` sh rabbitmq_config.sh ```
- Start Redis Server, run ``` redis-server ```
- Configure .aws/config & .aws/credentials
- Direct to repo directory /Celery_Lambda, run ```nohup celery -A proj worker -l info --concurrency=10 & ```
- Invoke Seneca ``` nohup seneca -m <model> -c ./config/<model>/config.py -l ./src/lambda_func/<model>/<model>.py -r 30 & ```
- Kill background celery workers ``` kill $(ps aux | grep '[c]elery' | awk '{print $2}') ```
- List celery queue ``` sudo rabbitmqctl list_queues celery -p myvhost ```
- Purge celery queue ``` sudo rabbitmqctl purge_queue celery -p myvhost ```


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