from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = Field(default="development", alias="SCENEMOTION_ENV")
    output_dir: Path = Field(default=Path("outputs"), alias="SCENEMOTION_OUTPUT_DIR")
    sample_dir: Path = Field(default=Path("sample_data/videos"), alias="SCENEMOTION_SAMPLE_DIR")
    max_upload_mb: int = Field(default=200, alias="SCENEMOTION_MAX_UPLOAD_MB")
    cors_origins: str = Field(default="http://localhost:3000", alias="SCENEMOTION_CORS_ORIGINS")
    worker_mode: str = Field(default="local", alias="SCENEMOTION_WORKER_MODE")
    depth_provider: str = Field(default="fallback", alias="SCENEMOTION_DEPTH_PROVIDER")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.output_dir.mkdir(parents=True, exist_ok=True)
    s.sample_dir.mkdir(parents=True, exist_ok=True)
    return s
