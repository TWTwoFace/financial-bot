from asyncpg.connection import Connection, connect
from asyncpg import Record
import json

from src.config import DB_HOST, DB_PORT, DB_NAME, DB_PASSWORD, DB_USERNAME


class Database:
    _connection: Connection

    async def connect(self):
        self._connection = await connect(
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )

        await self._connection.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )

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

    def __del__(self):
        self.disconnect()


database = Database()
