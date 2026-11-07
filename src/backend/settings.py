import os
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True, kw_only=True)
class DataBaseSettings:
    db_driver: str
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str

    @property
    def database_url(self) -> str:
        return f"{self.db_driver}://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


@dataclass(frozen=True, slots=True, kw_only=True)
class AppSettings:
    cors_origins: list[str]


@dataclass(frozen=True, slots=True, kw_only=True)
class JWTSettings:
    jwt_secret: str
    jwt_algorithm: str
    access_expires_minutes: int
    refresh_expires_minutes: int


@dataclass(frozen=True, slots=True, kw_only=True)
class RedisSettings:
    redis_host: str
    redis_port: int
    redis_password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RabbitmqSettings:
    rabbit_host: str
    rabbit_port: int
    rabbit_username: str
    rabbit_password: str
    rabbit_virtual_host: str

    @property
    def url(self) -> str:
        return (
            f"amqp://{self.rabbit_username}:{self.rabbit_password}"
            f"@{self.rabbit_host}:{self.rabbit_port}/{self.rabbit_virtual_host}"
        )


class SmtpSecurity(StrEnum):
    SSL = "ssl"
    STARTTLS = "starttls"
    NONE = "none"


@dataclass(frozen=True, slots=True, kw_only=True)
class SMTPSettings:
    smtp_host: str
    smtp_port: int
    smtp_login: str
    smtp_password: str
    smtp_security: SmtpSecurity


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    db: DataBaseSettings
    app: AppSettings
    jwt: JWTSettings
    redis: RedisSettings
    rabbitmq: RabbitmqSettings
    smtp_settings: SMTPSettings


def load_settings() -> Settings:
    return Settings(
        db=DataBaseSettings(
            db_driver=os.environ["DB_DRIVER"],
            db_name=os.environ["DB_NAME"],
            db_user=os.environ["DB_USER"],
            db_pass=os.environ["DB_PASS"],
            db_host=os.environ["DB_HOST"],
            db_port=os.environ["DB_PORT"],
        ),
        app=AppSettings(cors_origins=os.environ["CORS_ORIGINS"].split(",")),
        jwt=JWTSettings(
            jwt_secret=os.environ["JWT_SECRET"],
            jwt_algorithm=os.environ["JWT_ALGORITHM"],
            access_expires_minutes=int(os.environ["JWT_ACCESS_EXPIRATION_MINUTES"]),
            refresh_expires_minutes=int(os.environ["JWT_REFRESH_EXPIRATION_MINUTES"]),
        ),
        redis=RedisSettings(
            redis_host=os.environ["REDIS_HOST"],
            redis_port=int(os.environ["REDIS_PORT"]),
            redis_password=os.environ["REDIS_PASSWORD"],
        ),
        rabbitmq=RabbitmqSettings(
            rabbit_host=os.environ["RABBITMQ_HOST"],
            rabbit_port=int(os.environ["RABBITMQ_PORT"]),
            rabbit_username=os.environ["RABBITMQ_USER"],
            rabbit_password=os.environ["RABBITMQ_PASS"],
            rabbit_virtual_host=os.environ["RABBITMQ_VHOST"],
        ),
        smtp_settings=SMTPSettings(
            smtp_host=os.environ["SMTP_HOST"],
            smtp_port=int(os.environ["SMTP_PORT"]),
            smtp_login=os.environ["SMTP_LOGIN"],
            smtp_password=os.environ["SMTP_PASSWORD"],
            smtp_security=SmtpSecurity(os.environ["SMTP_SECURITY"].lower()),
        ),
    )
