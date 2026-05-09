from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://mushafi:mushafi@localhost:5432/mushafi"
    redis_url: str = "redis://localhost:6379"

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_jwt_secret: str = ""

    quran_foundation_api_base: str = "https://api.qurancdn.com/api/qdc"
    quran_foundation_api_key: str = ""

    cors_origins: list[str] = ["*"]

    redis_cache_ttl: int = 86400  # 24h


settings = Settings()
