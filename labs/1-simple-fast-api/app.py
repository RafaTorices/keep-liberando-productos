"""
Module for launch application
"""

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from application.app import StudentsServer
from config import config


class Container:
    """
    Class Container configure necessary methods for launch application
    """

    def __init__(self):
        self._db_name = config.MONGODB_DB
        self._db_handler = AsyncIOMotorClient(config.MONGODB_URL)[self._db_name]
        self._students_server = StudentsServer(config, self._db_handler)

    async def start_server(self):
        """Function for start server"""
        await self._students_server.run_server()


if __name__ == "__main__":
    container = Container()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(container.start_server(), loop=loop)
    loop.run_forever()
