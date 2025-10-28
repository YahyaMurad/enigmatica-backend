from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://enigmatica_user:enigmatica_pass@localhost/enigmatica_db"


settings = Settings()
