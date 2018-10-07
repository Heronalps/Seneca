from celery import Celery

app = Celery('proj',
              backend='rpc://', 
              broker='amqp://myuser:mypassword@localhost:5672/myvhost',
              include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True,
)
# app.conf.broker_heartbeat = 10

if __name__ == '__main__':
    app.start()