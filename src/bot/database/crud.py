from datetime import datetime

from aiogram.types import Message, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import ContentModel, MessageModel, UserModel


class CRUDBase:
    """CRUD Base class for database operations."""

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        instances = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return instances.scalars().first()

    async def get_multi(self, session: AsyncSession):
        instances = await session.execute(select(self.model))
        return instances.scalars().all()

    async def get_first(self, session: AsyncSession):
        instances = await session.execute(select(self.model))
        return instances.scalars().first()

    async def get_or_create(self, object_data, session: AsyncSession):
        instance = await self.get(object_data["id"], session)
        if instance:
            return instance

        instance = self.model(**object_data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

# class CRUDMessageData(CRUDBase):
#     """CRUD operations for MessageData objects."""

#     async def get_message_by_id(
#         self, message_id: int, session: AsyncSession
#     ):
#         db_obj = await session.execute(
#             select(self.model).where(self.model.id == message_id)
#         )
#         return db_obj.scalars().first()

#     async def update_message_data_attrib(
#         self, object: MessageModel, message: Message, session: AsyncSession
#     ):
#         object.text = getattr(message, "text", None)
#         object.sticker = getattr(message.sticker, "emoji", None)
#         object.timestamp = message.date
#         session.add(object)
#         await session.commit()
#         await session.refresh(object)
#         await session.close()


class UserManager(CRUDBase):
    """A class to manage users in a database."""

    async def add_user(
        self,
        user_data: User,
        session: AsyncSession
    ) -> UserModel:
        data = {
            "id": user_data.id,
            "username": user_data.username,
            "full_name": user_data.full_name
        }
        return await self.get_or_create(data, session)


class MessageManager(CRUDBase):
    """A class to manage messages in a database."""

    async def add_message(
        self,
        message_data: Message,
        session: AsyncSession
    ) -> MessageModel:
        data = {
            "id": message_data.message_id,
            "timestamp": message_data.date,
            "user_id": message_data.from_user.id,
        }
        return await self.get_or_create(data, session)


class ContentManager(CRUDBase):
    """A class to manage messages in a database."""

    async def add_content(
        self,
        message_data: Message,
        session: AsyncSession
    ) -> MessageModel:
        date = message_data.date
        if message_data.edit_date:
            date = datetime.utcfromtimestamp(message_data.edit_date)

        data = {
            "timestamp": date,
            "message_id": message_data.message_id,
            "text": message_data.text
        }
        instance = self.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


user_manager = UserManager(UserModel)
message_manager = MessageManager(MessageModel)
content_manager = ContentManager(ContentModel)
