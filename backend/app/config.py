from pydantic import BaseModel

try:
    _pydantic_settings = __import__(
        "pydantic_settings",
        fromlist=["BaseSettings", "SettingsConfigDict"],
    )
    BaseSettings = _pydantic_settings.BaseSettings
    SettingsConfigDict = _pydantic_settings.SettingsConfigDict
except ModuleNotFoundError:
    # Fallback for environments where pydantic-settings is unavailable.
    BaseSettings = BaseModel
    SettingsConfigDict = dict


class Settings(BaseSettings):
    LLM_API_BASE_URL: str = "https://aihubmix.com/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
