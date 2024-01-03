from celery import Celery

from config.celery import settings as celery_settings
from config.config import settings

celery_app: Celery = Celery(main=settings.NAME, broker=celery_settings.CELERY_BROKER_URL, task_ignore_result=True)

# 导入任务列表
import app.tasks.run_task  # noqa
