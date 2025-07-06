from asyncpg.connection import Connection, connect
from asyncpg import Record
import json

from src.config import *


class Database:
    _connection: Connection

    async def connect(self):
        self._connection = await connect(
            database=config.database.name,
            host=config.database.host,
            port=config.database.port,
            user=config.database.username,
            password=config.database.password
        )
        await self._connection.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        print("Database: connection opened")

    async def execute(self, query: str) -> None:
        await self._connection.execute(query)

    async def fetchone(self, query: str):
        response = await self._connection.fetchrow(query)
        return response

    async def fetchmany(self, query: str) -> list[Record]:
        response = await self._connection.fetch(query)
        return response

    async def disconnect(self) -> None:
        await self._connection.close()
        print("Database: connection closed")

    def __del__(self):
        self.disconnect()


database = Database()
