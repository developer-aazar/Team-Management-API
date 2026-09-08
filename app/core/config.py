from pydantic_settings import BaseSettings 


class Settings(BaseSettings):
    app_name: str 
    debug: bool 
    database_url: str 
    secret_key: str 
    algorithm: str 
    access_token_expire_minutes: int 
    refresh_token_expire_days: int 

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()