from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_hostname: str
    database_name: str
    database_username: str
    database_password: str
    database_port: int

    class Config:
        env_file = ".env"


settings = Settings()
