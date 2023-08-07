from pydantic import BaseSettings


class Settings(BaseSettings):
    id: str
    secret: str

    class Config:
        env_prefix = "HOSTEDPI_"
        env_file = ".env"
