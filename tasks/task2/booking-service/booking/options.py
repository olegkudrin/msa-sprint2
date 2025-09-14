from pydantic import BaseModel
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    host: str = "localhost"
    port: int = 5432
    username: str = "hotelio_booking"
    password: str = "hotelio_booking"
    dbname: str = "hotelio_booking"
    echo: bool = True

    @property
    def url(self):
        return (
            f"postgresql+psycopg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.dbname}"
        )


class Monolith(BaseModel):
    url: Url = Url("http://monolith:8080")


class Kafka(BaseModel):
    bootstrap_servers: str = "localhost:9092"
    history_topic: str = "booking_history"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOOKING_",
        env_nested_delimiter="__",
        nested_model_default_partial_update=True,
    )
    database: Database = Database()
    monolith: Monolith = Monolith()
    kafka: Kafka = Kafka()
    service_port: int = 9090


config = Settings()
