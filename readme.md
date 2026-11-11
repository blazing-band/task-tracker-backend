Transaction Inbox / Transaction Outbox

+ Дедубликация.

Создаем табличку с even_id и body и status.
При чтении открываем транзакцию записываем в бд event / проверить что такое еще не обработали.
А в воркере смотреть в эту табличку и отправлять на email.

- [ ] Transaction Inbox понять и реализовать
- [ ] Transaction Outbox понять и реализовать
- [ ] Запуск kafka consumer в отдельном процессе

celery start:
- worker - uv run --env-file .env celery -A src.backend.worker worker --pool=solo --loglevel=info
- beat - uv run --env-file .env celery -A src.backend.worker beat
