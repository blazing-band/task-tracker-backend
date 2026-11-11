from celery import shared_task
from dishka import FromDishka
from dishka.integrations.celery import inject

from backend.celery_app import CeleryTaskName
from backend.services import EmailService


@shared_task(name=CeleryTaskName.SEND_USER_REGISTERED_EMAIL)
@inject
def send_user_registered_email(
    email: str,
    email_service: FromDishka[EmailService],
) -> None:
    email_service.send_message(
        subject="Welcome to Task Tracker!",
        body="Your account has been successfully created.",
        destination_email=email,
    )
