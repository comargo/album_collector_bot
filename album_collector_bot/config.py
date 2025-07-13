"""
This module contains application settings.

Settings can be loaded from environment variables or from .env file.
"""

import os
import argparse
from collections.abc import Sequence

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings.

    Attributes:
        LOG_LEVEL: str = Log level. Default is "INFO".

        BOT_TOKEN: str = Telegram bot token. Required.
        REDIS_URL: Optional[str] = Redis URL.

        WEBHOOK_IP: Optional[str] = Webhook IP address. If not set, bot will run in long polling mode.
        WEBHOOK_PORT: int = Webhook port. Default is 8080.
        WEBHOOK_PATH: str = Webhook path. Default is "/webhook".
        WEBHOOK_SECRET_TOKEN: Optional[str] = Webhook secret token.
        WEBHOOK_URL: Optional[str] = Webhook URL.

        YDB_ENDPOINT: Optional[str] = YDB endpoint.
        YDB_DATABASE: Optional[str] = YDB database.
        YDB_TABLE_PREFIX: str = YDB table prefix. Default is "album_creator_bot".
    """

    def __init__(self, args: Sequence[str] | None = None) -> None:
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

        # Telegram bot settings
        # BOT_TOKEN could be set in environment variable or passed as argument
        self._BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
        
        # Redis settings
        self.REDIS_URL: str | None = os.getenv("REDIS_URL")

        # Webhook settings
        self.WEBHOOK_IP: str | None = os.getenv("WEBHOOK_IP")
        try:
            self.WEBHOOK_PORT: int = int(os.environ.get("WEBHOOK_PORT", "8080"))
        except ValueError as exc:
            raise ValueError("WEBHOOK_PORT must be an integer.") from exc
        self.WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/webhook")
        self.WEBHOOK_SECRET_TOKEN: str | None = os.getenv("WEBHOOK_SECRET_TOKEN")
        self.WEBHOOK_URL: str | None = os.getenv("WEBHOOK_URL")

        # YDB settings
        self.YDB_ENDPOINT: str | None = os.getenv("YDB_ENDPOINT")
        self.YDB_DATABASE: str | None = os.getenv("YDB_DATABASE")
        self.YDB_TABLE_PREFIX: str = os.getenv("YDB_TABLE_PREFIX", "album_creator_bot")
        
        if args:
            self.parse_args(args=args)
    
    @property
    def BOT_TOKEN(self) -> str:
        """
        Get bot token.
        """
        if not self._BOT_TOKEN:
            raise RuntimeError("Bot token is not set. Please set BOT_TOKEN environment variable.")
        else:
            return self._BOT_TOKEN

    @property
    def use_ydb(self) -> bool:
        """
        Check if YDB is used.

        Returns:
            bool: True if YDB is used, False otherwise.
        """
        return (
            isinstance(self.YDB_ENDPOINT, str)
            and isinstance(self.YDB_DATABASE, str)
            and self.YDB_ENDPOINT.strip() != ""
            and self.YDB_DATABASE.strip() != ""
        )

    def parse_args(self, args: Sequence[str] | None = None) -> None:
        """
        Parse command line arguments.
        """
        parser = argparse.ArgumentParser(
            prog="AlbumCreatorBot",
            description="AlbumCreatorBot is a Telegram bot that allows you to create albums of photos and videos.",
        )
        parser.add_argument(
            "--log-level", "-l", type=str, help="Log level.", dest="LOG_LEVEL"
        )
        parser.add_argument(
            "--bot-token", "-t", type=str, help="Telegram bot token.", dest="_BOT_TOKEN"
        )
        parser.add_argument(
            "--redis-url", "-r", type=str, help="Redis URL.", dest="REDIS_URL"
        )
        parser.add_argument(
            "--webhook-ip",
            "-i",
            type=str,
            help="Webhook IP address.",
            dest="WEBHOOK_IP",
        )
        parser.add_argument(
            "--webhook-port", "-p", type=int, help="Webhook port.", dest="WEBHOOK_PORT"
        )
        parser.add_argument(
            "--webhook-path", "-w", type=str, help="Webhook path.", dest="WEBHOOK_PATH"
        )
        parser.add_argument(
            "--webhook-secret-token",
            "-s",
            type=str,
            help="Webhook secret token.",
            dest="WEBHOOK_SECRET_TOKEN",
        )
        parser.add_argument(
            "--webhook-url", "-u", type=str, help="Webhook URL.", dest="WEBHOOK_URL"
        )
        parser.add_argument(
            "--ydb-endpoint", "-e", type=str, help="YDB endpoint.", dest="YDB_ENDPOINT"
        )
        parser.add_argument(
            "--ydb-database", "-d", type=str, help="YDB database.", dest="YDB_DATABASE"
        )
        parser.add_argument(
            "--ydb-table-prefix",
            "-x",
            type=str,
            help="YDB table prefix.",
            dest="YDB_TABLE_PREFIX",
        )

        parser.parse_args(args=args, namespace=self)
