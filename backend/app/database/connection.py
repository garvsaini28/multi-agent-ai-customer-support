from pymongo import MongoClient
from app.core.config import settings


# ============================================================
# MONGODB CLIENT
# ============================================================

client = MongoClient(
    settings.MONGODB_URL,

    # Connection timeout
    serverSelectionTimeoutMS=30000,

    # Socket timeout
    socketTimeoutMS=30000,

    # Connection timeout
    connectTimeoutMS=30000,

    # Retry failed reads/writes
    retryReads=True,
    retryWrites=True
)


# ============================================================
# DATABASE
# ============================================================

db = client[settings.DATABASE_NAME]


# ============================================================
# DATABASE ACCESS
# ============================================================

def get_database():

    return db