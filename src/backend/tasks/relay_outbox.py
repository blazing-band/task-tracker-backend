import logging
from typing import Any, Callable

from celery import shared_task
from dishka import FromDishka
from dishka.integrations.celery import inject

from backend.celery_app import CeleryTaskName
from backend.entities import EventStatus, EventType
from backend.repositories import SyncOutboxRepository
from backend.tasks import send_user_registered_email

logger = logging.getLogger(__name__)


def _send_user_created_email(payload: dict[str, Any]) -> None:
    send_user_registered_email.delay(**payload)  # type: ignore[attr-defined]


event_mapper: dict[EventType, Callable[[dict[str, Any]], None]] = {
    EventType.USER_CREATED: _send_user_created_email
}


@shared_task(name=CeleryTaskName.OUTBOX_RELAY)
@inject
def relay_outbox(
    outbox_repository: FromDishka[SyncOutboxRepository],
) -> None:
    outbox_batch = outbox_repository.get_batch()
    if not outbox_batch:
        return

    for outbox in outbox_batch:
        handler = event_mapper.get(outbox.event_type)
        if handler is None:
            logger.warning("No handler for event type %s (outbox id=%s)", outbox.event_type, outbox.id)
            continue

        handler(outbox.payload)

        outbox_repository.change_status(outbox.id, EventStatus.SENT)
        outbox_repository.session.commit()
