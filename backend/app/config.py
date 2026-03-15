from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_env: str = 'development'
    database_url: str = 'postgresql+psycopg://postgres:postgres@db:5432/science_concierge'
    secret_key: str = 'change-me'
    openai_api_key: str | None = None
    openai_model: str = 'gpt-4o-mini'
    storage_dir: str = '/data/uploads'
    payment_provider: str = 'yookassa'
    payment_shop_id: str | None = None
    payment_secret_key: str | None = None


settings = Settings()
