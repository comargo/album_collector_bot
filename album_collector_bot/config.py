"""
This module contains application settings.

Settings can be loaded from environment variables or from .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings.

    Attributes:
        BOT_TOKEN: str = Telegram bot token.
        REDIS_URL: Optional[str] = Redis URL.
        MAX_MEDIA_IN_ALBUM: int = Max number of media in album. Default is 10.
        WEBHOOK_HOST: Optional[str]  = Webhook host.
        WEBHOOK_PATH: str = Webhook path. Default is "/webhook".
        WEBHOOK_URL: Optional[str] = Webhook URL.
        WEBAPP_HOST: str = Webhook host. Default is "0.0.0.0".
        WEBAPP_PORT: int = Webhook port. Default is 8000.
        YDB_ENDPOINT: Optional[str] = YDB endpoint.
        YDB_DATABASE: Optional[str] = YDB database.
        YDB_TABLE_PREFIX: str = YDB table prefix. Default is "albumbot".

        Attributes of this class can be accessed as attributes of the `settings` object.
    """
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Telegram bot settings
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    REDIS_URL: str | None = os.getenv("REDIS_URL")

    # Webhook settings
    WEBHOOK_HOST: str | None = os.getenv("WEBHOOK_HOST")
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
    WEBHOOK_URL: str | None = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST else None

    # Server settings
    WEBAPP_HOST: str = os.getenv("WEBAPP_HOST", "0.0.0.0")
    WEBAPP_PORT: int = int(os.getenv("WEBAPP_PORT", "8000"))

    # YDB settings
    YDB_ENDPOINT: str | None = os.getenv("YDB_ENDPOINT")
    YDB_DATABASE: str | None = os.getenv("YDB_DATABASE")
    YDB_TABLE_PREFIX: str = os.getenv("YDB_TABLE_PREFIX", "albumbot")

    def __init__(self) -> None:
        assert self.BOT_TOKEN, "BOT_TOKEN must be set!"

    @property
    def use_ydb(self) -> bool:
        """
        Check if YDB is used.

        Returns:
            bool: True if YDB is used, False otherwise.
        """
        return bool(self.YDB_ENDPOINT and self.YDB_DATABASE)


settings = Settings()
