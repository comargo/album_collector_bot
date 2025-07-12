"""
Bot application entry point
"""

import string
import secrets

from telegram.constants import UpdateType

from album_collector_bot import create_app
from album_collector_bot.config import Settings

MIN_TOKEN_LENGTH = 32
MAX_TOKEN_LENGTH = 256


def generate_token_secure(length=None):
    """
    Генерирует криптографически безопасный токен.
    Если длина не указана, выбирается случайное значение от 32 до 256.
    Минимальная длина токена — 32 символа.
    Использует модуль secrets для более высокой безопасности.

    :param length: Длина токена (если не указана, выбирается случайно)
    :return: Строка-токен
    """

    if length is None:
        length = (
            secrets.randbelow(MAX_TOKEN_LENGTH - MIN_TOKEN_LENGTH + 1)
            + MIN_TOKEN_LENGTH
        )
    elif length < MIN_TOKEN_LENGTH:
        raise ValueError(
            f"Token length must be at least {MIN_TOKEN_LENGTH} characters for security."
        )

    return secrets.token_urlsafe(length)[:length]


def main():
    """
    Main function
    """
    settings = Settings()
    settings.parse_args()
    app = create_app(settings=settings)
    allowed_updates = [
        UpdateType.MESSAGE,
        UpdateType.CALLBACK_QUERY,
        UpdateType.EDITED_MESSAGE,
    ]
    if settings.WEBHOOK_IP:
        if not settings.WEBHOOK_SECRET_TOKEN:
            settings.WEBHOOK_SECRET_TOKEN = generate_token_secure(32)

        app.run_webhook(
            listen=settings.WEBHOOK_IP,
            port=settings.WEBHOOK_PORT,
            url_path=settings.WEBHOOK_PATH,
            secret_token=settings.WEBHOOK_SECRET_TOKEN,
            allowed_updates=allowed_updates,
        )
    else:
        app.run_polling(
            allowed_updates=allowed_updates,
        )


if __name__ == "__main__":
    main()
