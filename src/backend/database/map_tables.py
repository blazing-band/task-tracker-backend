from .models import map_task_table, map_user_table


def map_tables() -> None:
    map_user_table()
    map_task_table()
