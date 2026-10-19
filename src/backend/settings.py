import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class DataBaseSettings:
    db_driver: str
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str

    @property
    def database_url(self):
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
class Settings:
    db: DataBaseSettings
    app: AppSettings
    jwt: JWTSettings
    redis: RedisSettings


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
    )
