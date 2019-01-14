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

## Prophet

* Install Prophet in virtual environment
```
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install fbprophet --no-cache
```

* Run local container to build up lambda package
```
docker run -it lambci/lambda:build-python3.6 bash
```
```
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install fbprophet --no-cache
```
```
pip uninstall -y matplolib
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "test" | xargs rm -rf
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "tests" | xargs rm -rf
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/src"
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/lib/stan_math/lib"
echo "venv size $(du -sh $VIRTUAL_ENV | cut -f1)"
```
```
cd /var/task/Celery_Lambda/venv/lib/python3.6/site-packages
zip -9rq /var/task/lambda.zip *
cd /var/task/Celery_Lambda/src/lambda_func/
zip -9 /var/task/lambda.zip prophet.py
```
```
# At MacOS terminal
sudo docker ps # Get container ID
docker cp <containerId>:/var/task/lambda.zip ~/Downloads
```
