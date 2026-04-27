from pydantic_settings import BaseSettings
"""
Application settings loader using Pydantic BaseSettings.

This module defines a settings class that reads secrets, token settings, and
database connection parameters from environment variables. The common problem
with this approach is that the `.env` file location is computed relative to the
source file, so if the code is executed from a different working directory or
the file layout changes, the `.env` file may not be found and settings will not
load correctly.

Solution:
- Ensure the `.env` file exists at the expected project root.
- Use a stable path calculation such as `Path(__file__).resolve().parents[1] / ".env"`
    or configure `env_file = ".env"` with the working directory set correctly.
- Verify that `Settings()` is instantiated after the path is resolved correctly
    so environment variables are loaded as intended.
"""
from pathlib import Path


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    database_hostname: str
    database_name: str
    database_username: str
    database_password: str
    database_port: int

    model_config = {
        "env_file": Path(__file__).resolve().parent.parent / ".env"
    }


settings = Settings() # type: ignore

