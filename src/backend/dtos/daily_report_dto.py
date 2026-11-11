from dataclasses import dataclass

# Message contract of the daily report Kafka topic (same as in task-tracker-scheduler)


@dataclass(frozen=True, slots=True, kw_only=True)
class DailyReportUserDto:
    email: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DailyReportTaskDto:
    name: str
    text: str
    status: str
    timestamp: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DailyReportDto:
    user: DailyReportUserDto
    tasks: list[DailyReportTaskDto]
