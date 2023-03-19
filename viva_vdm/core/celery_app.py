from celery import Celery
from viva_vdm.core.settings import ResourceConfig

settings = ResourceConfig()

tasks = ['viva_vdm.core.tasks']

app = Celery(
    'viva_vdm.core.celery_app',
    include=tasks,
    broker=F'amqp://{settings.rabbitmq_username}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:5672',
)

app.autodiscover_tasks(['viva_vdm.core.tasks'])


def main():
    worker = app.Worker(include=tasks, pool='solo', loglevel='debug')
    worker.start()


if __name__ == "__main__":
    main()
