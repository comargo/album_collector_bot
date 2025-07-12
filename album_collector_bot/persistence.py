"""

"""

from telegram.ext import DictPersistence
from .config import Settings

def get_persistence(settings: Settings):
    # if settings.use_ydb:
    #     return YDBPersistence()
    # if settings.REDIS_URL:
    #     return RedisPersistence()
    # else:
    return DictPersistence()

