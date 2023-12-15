"""
Module for define config used by app when running tests
"""

import os
from mongomock_motor import AsyncMongoMockClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://user:aa@localhost:27017/")
MONGODB_ENGINE = AsyncMongoMockClient()
MONGODB_DB = "college"
MONGODB_COLLECTION = "students"
