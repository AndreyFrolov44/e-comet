import typing

from databases import Database
from sqlalchemy import Table


class BaseService:
    def __init__(self, database: Database, table: Table):
        self.database = database
        self.table = table

    async def create(self, *args, **kwargs) -> typing.Any:
        query = self.table.insert().values(*args, **kwargs)
        return await self.database.execute(query)

    async def get(self, *args, **kwargs) -> typing.Any:
        query = self.table.select().where(*args, **kwargs)
        return await self.database.fetch_one(query)
