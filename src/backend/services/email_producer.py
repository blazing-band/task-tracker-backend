# TODO: celery is disabled for now
# from celery import Celery

# from backend.entities import User


# class EmailProducer:
#     def __init__(self, celery_app: Celery) -> None:
#         self.celery_app = celery_app

#     def send_user_registration_email(self, user: User) -> None:
#         subject = "Welcome to Task Tracker!"
#         message = "Your account has been successfully created."
#         self.celery_app.send_task(
#             "email_sender.send_user_registered_email",
#             exchange="email",
#             routing_key="registration_email",
#             kwargs={"email": user.email, "subject": subject, "message": message},
#         )
