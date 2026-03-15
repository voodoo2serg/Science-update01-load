from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    app_env: str = 'production'
    app_name: str = 'Science Concierge'
    secret_key: str = 'change-me-in-production'
    database_url: str = 'postgresql+psycopg://postgres:postgres@db:5432/science_concierge'
    openai_api_key: str | None = None
    openai_model: str = 'gpt-4o-mini'
    storage_dir: str = '/data/uploads'
    max_upload_size_mb: int = 25
    allowed_extensions: str = '.pdf,.docx,.txt'
    payment_provider: str = 'demo'
    payment_shop_id: str | None = None
    payment_secret_key: str | None = None
    yookassa_webhook_secret: str | None = None
    cors_origins: str = 'http://localhost,http://127.0.0.1'

    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if value == 'change-me-in-production':
            return value
        if len(value) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(',') if item.strip()]

    @property
    def allowed_extensions_set(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_extensions.split(',') if item.strip()}


settings = Settings()
