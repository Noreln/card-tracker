from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/card_tracker"
    tcgplayer_api_key: str = ""
    tcgplayer_private_key: str = ""
    cardmarket_app_token: str = ""
    cardmarket_app_secret: str = ""
    cardmarket_access_token: str = ""
    cardmarket_access_secret: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
