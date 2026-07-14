from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    lm_studio_base_url: str
    lm_studio_model: str
    lm_studio_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()