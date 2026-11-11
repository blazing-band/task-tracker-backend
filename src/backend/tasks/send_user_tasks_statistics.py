import logging

from celery import shared_task
from dishka import FromDishka
from dishka.integrations.celery import inject

from backend.celery_app import CeleryTaskName
from backend.dtos import DailyReportDto, DailyReportTaskDto, DailyReportUserDto
from backend.repositories import SyncTaskRepository
from backend.services import DailyReportProducer

logger = logging.getLogger(__name__)


@shared_task(name=CeleryTaskName.SEND_USER_TASKS_STATISTICS)
@inject
def send_user_tasks_statistics(
    task_repository: FromDishka[SyncTaskRepository],
    daily_report_producer: FromDishka[DailyReportProducer],
) -> None:
    for user in task_repository.get_all_users():
        tasks = task_repository.get_user_tasks_for_previous_day(user.id)
        if not tasks:
            continue
        daily_report_producer.send(
            DailyReportDto(
                user=DailyReportUserDto(email=user.email),
                tasks=[
                    DailyReportTaskDto(
                        name=task.name,
                        text=task.text,
                        status=task.status,
                        timestamp=task.timestamp.isoformat(),
                    )
                    for task in tasks
                ],
            )
        )
    daily_report_producer.flush()
