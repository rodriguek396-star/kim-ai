from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    cors_origins: str = "http://localhost:5173"
    storage_mode: str = "sqlite"
    sqlite_path: str = "./kim.db" 
    snowflake_account: str = "" 
    snowflake_user: str = ""
    snowflake_password: str = ""
    snowflake_warehouse: str = ""
    snowflake_database: str = "KIM_DB"
    snowflake_schema: str = "PUBLIC"
    snowflake_role: str = ""
    ai_provider: str = "none"
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    cortex_model: str = "mistral-large2"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
