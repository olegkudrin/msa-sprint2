from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    host: str = "localhost"
    port: int = 5432
    username: str = "hotelio_history"
    password: str = "hotelio_history"
    dbname: str = "hotelio_history"
    echo: bool = True

    @property
    def url(self):
        return (
            f"postgresql+psycopg://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.dbname}"
        )


class Kafka(BaseModel):
    bootstrap_servers: str = "localhost:9092"
    history_topic: str = "booking_history"
    group_id: str = "history"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOOKING_HISTORY_",
        env_nested_delimiter="__",
        nested_model_default_partial_update=True,
    )
    database: Database = Database()
    kafka: Kafka = Kafka()


config = Settings()
