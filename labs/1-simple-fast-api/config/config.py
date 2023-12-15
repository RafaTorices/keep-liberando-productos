"""
Module for define config used by app
"""

import os

FASTAPI_CONFIG = {
    "port": 8081,
}
MONGODB_URL = os.environ["MONGODB_URL"]
MONGODB_DB = "college"
MONGODB_COLLECTION = "students"
