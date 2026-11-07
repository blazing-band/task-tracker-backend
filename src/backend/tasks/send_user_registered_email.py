from celery import shared_task
from dishka import FromDishka
from dishka.integrations.celery import inject

from backend.celery_app import CeleryTaskName
from backend.services import EmailService


@shared_task(name=CeleryTaskName.SEND_USER_REGISTERED_EMAIL)
@inject
def send_user_registered_email(
    email: str,
    subject: str,
    message: str,
    email_service: FromDishka[EmailService],
) -> None:
    email_service.send_message(
        subject=subject,
        body=message,
        destination_email=email,
    )
