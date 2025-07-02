"""

"""

from telegram.ext import DictPersistence
from .config import settings

def get_persistence():
    # if settings.use_ydb:
    #     return YDBPersistence()
    # if settings.REDIS_URL:
    #     return RedisPersistence()
    # else:
    return DictPersistence()

