from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Smart Plug IoT Server"

    API_VERSION: str = "v1"

    DATABASE_URL: str = "sqlite:///smartplug.db"

    MQTT_HOST: str = "127.0.0.1"

    MQTT_PORT: int = 1883

    MQTT_KEEPALIVE: int = 60

    MQTT_USERNAME: str | None = None

    MQTT_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()