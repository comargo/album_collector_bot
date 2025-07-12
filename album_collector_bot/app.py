"""
This module contains the Telegram bot application.
"""

import logging

from telegram.ext import Application

from .config import Settings
from .handlers import handlers
from .persistence import get_persistence
from .context import custom_context_types

async def _post_init(application: Application) -> None:
    """
    Post initialization hook.
    """
    await application.bot.set_my_commands([
        ('start', 'Starts the bot'),
        ('collect', 'Collects the album from user\'s media and description'),
        ('reset', 'Forget sent media and description'),
        ])

def create_app(settings:Settings|None = None) -> Application:
    """Create the telegram bot application."""

    settings = settings or Settings()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=settings.LOG_LEVEL,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    application = (
        Application.builder()
        .token(settings.BOT_TOKEN)
        .persistence(get_persistence(settings))
        .context_types(custom_context_types)
        .post_init(_post_init)
        .build()
    )

    application.add_handlers(handlers)
    return application
