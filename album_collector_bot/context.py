"""
Module for defining custom callback context.
"""

from dataclasses import dataclass, field
from telegram.ext import ContextTypes, CallbackContext, ExtBot
from telegram import InputMediaPhoto, InputMediaVideo


@dataclass
class MediaItem:
    """
    Class for storing media item.
    """

    item: InputMediaPhoto | InputMediaVideo
    message_id: int
    
@dataclass
class CaptionItem:
    """
    Class for storing description item.
    """
    caption: str
    message_id: int


@dataclass
class UserData:
    """
    Class for storing user data.
    """

    media_messages: list[MediaItem] = field(default_factory=list)
    caption_message: CaptionItem | None = None

    def clear(self):
        """
        Clear all media messages and description.
        """
        self.media_messages.clear()
        self.caption_message = None


class CustomContext(CallbackContext[ExtBot, UserData, dict, dict]):
    """
    Custom callback context.
    """


custom_context_types = ContextTypes(context=CustomContext, user_data=UserData)
