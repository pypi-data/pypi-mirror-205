from typing import Any, ClassVar

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy import MetaData, Table, Column, Integer, Text, String, DateTime, Date, select
from sqlalchemy.sql import Select
from sqlalchemy.orm import declarative_base
from .model import Model as DefaultModel, DefaultMeta
from .migrate import Migration
from asyncio import run
from fastapi import FastAPI, Request
from .middleware import Middleware


class SQLAlchemy:
    __engine__: AsyncEngine
    session: AsyncSession
    __metadata__: MetaData
    migration: Migration
    __naming_conventions__: 'dict[str, str]' = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    __closed__ = False
    
    middleware = Middleware
    
    Model: DefaultModel
    Table = Table
    
    Column = Column
    Integer = Integer
    Text = Text
    String = String
    DateTime = DateTime
    Date = Date
    
    def __init__(self, app: FastAPI, *, database_uri: str, session_options: 'dict[str,Any]' = {}, **kwargs
    ):
        self.__engine__ = create_async_engine(database_uri)
        self.__sessionmaker__ = async_sessionmaker(
                    bind=self.__engine__, 
                    autoflush=session_options.get('session_autoflush', True),
                    expire_on_commit=session_options.get('expire_on_commit', True)
        )
        if kwargs.get('naming_convention') is not None:
            self.__naming_conventions__ = kwargs.get('naming_convention', {})
        self.__metadata__ = MetaData(naming_convention=self.__naming_conventions__)
        self.Model = self._make_declarative_base() # type: ignore
        if kwargs.get('migrate', False):
            self.migration = Migration(kwargs.get('migration_options', {}))
            
        if app is not None:
            app.add_middleware(self.middleware, sqlalchemy=self)
            
        
    async def create_all(self):
        async with self.__engine__.begin() as conn:
            await conn.run_sync(self.__metadata__.create_all)
        
    select:Select[Any] = select # type: ignore
    
    def _make_declarative_base(self) -> 'type[DefaultModel]':
        model = declarative_base(
            metadata=self.__metadata__,
            cls=DefaultModel,
            name="Model",
            metaclass=DefaultMeta # type: ignore
        )
        return model