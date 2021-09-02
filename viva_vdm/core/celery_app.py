from celery import Celery
from .settings import ResourceConfig

settings = ResourceConfig()

tasks = ['viva_ddm.core.tasks']

app = Celery(
    'viva_ddm.celery_app',
    include=tasks,
    broker=F'amqp://{settings.rabbitmq_username}:{settings.rabbitmq_password}@{settings.rabbitmq_host}:5672',
)

app.autodiscover_tasks(['viva_ddm.core.tasks'])


def main():
    worker = app.Worker(include=tasks, pool='solo', loglevel='debug')
    worker.start()


if __name__ == "__main__":
    main()
