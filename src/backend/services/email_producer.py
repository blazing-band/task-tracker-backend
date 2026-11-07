from celery import Celery

from backend.celery_app import CeleryTaskName


class EmailProducer:
    def __init__(self, celery_app: Celery) -> None:
        self.celery_app = celery_app

    def send_user_registration_email(self, email: str) -> None:
        subject = "Welcome to Task Tracker!"
        message = "Your account has been successfully created."
        # Exchange and routing key come from task_routes in create_celery
        self.celery_app.send_task(
            CeleryTaskName.SEND_USER_REGISTERED_EMAIL,
            kwargs={"email": email, "subject": subject, "message": message},
        )
