"""
This module contains handlers for Telegram commands and messages.

It defines the following functions:
    - cmd_start: Handles the /start command.
    - add_media: Handles messages containing media.
    - add_description: Handles messages containing a description.
    - cmd_collect: Handles the /collect command.
    - cmd_reset: Handles the /reset command.

    These functions are registered in the main.py module using the Dispatcher
    class to handle incoming Telegram commands and messages.
"""

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    BaseHandler,
    filters,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
    Chat,
)
from telegram.error import TelegramError
from telegram.constants import MediaGroupLimit
from .context import CustomContext, MediaItem, CaptionItem

import logging

logger = logging.getLogger(__name__)

QUERY_DELETE = "delete"


async def cmd_start(update: Update, context: CustomContext) -> None:
    """
    Handles the /start command.

    This function sends a welcome message to the user and resets the user's
    album data in the UserContext.
    """
    assert update.effective_message
    assert context.user_data is not None
    context.user_data.media_messages.clear()
    context.user_data.caption_message = None
    try:
        await update.effective_message.reply_text(
            "Welcome to Album Collector! Please send me a photo or a video and "
            "description to start collecting your album."
        )
    except TelegramError:
        logger.exception("Failed to send welcome message")


def _get_message_media(message: Message):
    if message.photo:
        return InputMediaPhoto(message.photo[-1], message.caption)
    elif message.video:
        return InputMediaVideo(message.video, message.caption)
    else:
        logger.warning("Unsupported media type in message: %s",message.message_id)
        return None


async def add_media(update: Update, context: CustomContext) -> None:
    """
    Handles messages containing media.

    This function appends the received media to the user's album data in the
    UserContext.
    """
    assert update.effective_message
    assert context.user_data is not None

    item = _get_message_media(update.effective_message)
    if not item:
        try:
            await update.effective_message.reply_text("Please send me a photo or a video.")
        except TelegramError:
            logger.exception("Failed to send error message")
        return

    try:
        # Copy method returns a message ID of copied message
        new_message_id = await update.effective_message.copy(
            update.effective_message.chat_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Delete",
                            callback_data=QUERY_DELETE,
                        )
                    ]
                ]
            ),
        )
        context.user_data.media_messages.append(MediaItem(item, new_message_id.message_id))
        await update.effective_message.delete()
    except TelegramError:
        logger.exception("Failed to send media")


async def delete_media(update: Update, context: CustomContext) -> None:
    """
    Handles the delete button click.
    """
    assert update.callback_query
    await update.callback_query.answer()

    assert context.user_data is not None
    assert update.effective_message
    for media in list(context.user_data.media_messages):
        if media.message_id == update.effective_message.message_id:
            context.user_data.media_messages.remove(media)
            break
    try:
        await update.callback_query.delete_message()
    except TelegramError:
        logger.exception("Failed to delete message")


async def add_description(update: Update, context: CustomContext) -> None:
    """
    Handles messages containing a description.
    """
    assert update.effective_message
    assert context.user_data is not None
    if update.effective_message.text:
        context.user_data.caption_message = CaptionItem(
            caption=update.effective_message.text,
            message_id=update.effective_message.message_id,
        )


async def update_message(update: Update, context: CustomContext) -> None:
    """
    Handles edited messages.
    """
    assert update.effective_message
    assert context.user_data is not None
    if update.effective_message.photo or update.effective_message.video:
        for media in context.user_data.media_messages:
            if media.message_id == update.effective_message.message_id:
                item = _get_message_media(update.effective_message)
                if item:
                    media.item = item
    elif update.effective_message.text:
        if context.user_data.caption_message:
            if (
                update.effective_message.message_id
                == context.user_data.caption_message.message_id
            ):
                context.user_data.caption_message.caption = (
                    update.effective_message.text
                )


async def _clear_album_data(context: CustomContext, chat: Chat | None) -> None:
    if not context.user_data:
        return
    try:
        if chat:
            message_ids = [
                message.message_id for message in context.user_data.media_messages
            ]
            if context.user_data.caption_message:
                message_ids.append(context.user_data.caption_message.message_id)
            await context.bot.delete_messages(chat.id, message_ids)
    except TelegramError:
        logger.exception("Failed to delete messages")
    context.user_data.clear()


async def cmd_collect(update: Update, context: CustomContext) -> None:
    """
    Handles the /collect command.

    This function collects the user's album data and sends it to the user.
    """
    assert update.effective_message
    assert update.effective_chat

    assert context.user_data is not None
    media = [message.item for message in context.user_data.media_messages]
    if not (
        MediaGroupLimit.MIN_MEDIA_LENGTH
        <= len(media)
        <= MediaGroupLimit.MAX_MEDIA_LENGTH
    ):
        await update.effective_message.reply_text(
            f"Please send me between {MediaGroupLimit.MIN_MEDIA_LENGTH} "
            f"and {MediaGroupLimit.MAX_MEDIA_LENGTH} media files before using /collect.\n"
            "You can add more media by sending more photos or videos.\n"
            "To remove media, you can delete your previous messages or use the /reset command to start over."
        )
        return

    if context.user_data.caption_message:
        # media is not empty, checked above
        if media[0].type == "photo":
            media[0] = InputMediaPhoto(
                media[0].media, context.user_data.caption_message.caption
            )
        elif media[0].type == "video":
            media[0] = InputMediaVideo(
                media[0].media, context.user_data.caption_message.caption
            )
    try:
        await update.effective_message.reply_media_group(media)
        await _clear_album_data(context, update.effective_chat)
    except TelegramError:
        logger.exception("Failed to send media group")


async def cmd_reset(update: Update, context: CustomContext) -> None:
    """
    Handles the /reset command.

    This function resets the user's album data in the UserContext.
    """
    await _clear_album_data(context, update.effective_chat)
    if update.effective_message:
        await update.effective_message.reply_text("Album data has been reset.")


handlers: list[BaseHandler] = [
    CommandHandler("start", cmd_start),
    CommandHandler("collect", cmd_collect),
    CommandHandler("reset", cmd_reset),
    MessageHandler(filters.VIDEO | filters.PHOTO, add_media),
    MessageHandler(filters.TEXT, add_description),
    MessageHandler(filters.UpdateType.EDITED, update_message),
    CallbackQueryHandler(pattern=QUERY_DELETE, callback=delete_media),
]
