from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    hindsight_api_key: str
    hindsight_base_url: str = "https://api.hindsight.vectorize.io"
    hindsight_bank_id: str = "dealmind"
    
    groq_api_key: str
    groq_model: str = "llama3-70b-8192"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
