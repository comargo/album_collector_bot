"""
Bot application entry point
"""

from telegram.constants import UpdateType

from album_collector_bot import create_app

app = create_app()

if __name__ == "__main__":
    app.run_polling(allowed_updates=[UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY, UpdateType.EDITED_MESSAGE])
