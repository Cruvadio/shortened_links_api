import datetime
import random
from typing import Generic, TypeVar, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base
from .models import Link
from sqlalchemy import select
from pydantic import BaseModel
from fastapi import HTTPException
T = TypeVar("T", bound=Base)
class BaseDAO(Generic[T]):
    model: type[T]  # Устанавливается в дочернем классе

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **kwargs):
        try:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, **kwargs):
        try:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: BaseModel):
        values_dict = values.model_dump()
        try:
            record = await session.get(cls.model, data_id)
            if not record:
                raise HTTPException(status_code=404,
                                    detail=f"Entry of class {cls.model.__class__.__name__} and id={data_id} has been not found")
            for key, value in values_dict.items():
                if value:
                    setattr(record, key, value)
            await session.commit()
            return record
        except SQLAlchemyError as e:
            print(e)
            raise e

    @classmethod
    async def delete_one_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.commit()
            else:
                raise HTTPException(status_code=404,
                                    detail=f"Entry of class {cls.model.__class__.__name__} and id={data_id} has been not found")
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise

class LinkDAO(BaseDAO[Link]):
    model = Link

    letters = 'abcdefghijklmnopqrstuvwxyz'
    shortened_length = 8

    @classmethod
    async def shorten_link(cls, session: AsyncSession, url: str):
        existing = await cls.find_one_or_none(session, original_url=url)
        if existing:
            return {"shortened_id": existing.shortened_id }
        short_url = ""
        for i in range(cls.shortened_length):
            short_url += random.choice(cls.letters)

        new_url = await cls.add(session, shortened_id=short_url, original_url=url)

        return {"shortened_id": short_url}

