from celery.signals import after_setup_logger

from app.providers import logging_provider

from app.providers.celery_app import celery_app  # noqa


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logging_provider.register()
