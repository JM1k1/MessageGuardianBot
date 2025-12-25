from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import (
    ChatModel,
    ContentModel,
    MessageModel,
    UserModel,
)


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


class UserManager(CRUDBase):
    """A class to manage users in a database."""

    async def add_user(
        self,
        user_data,
        session: AsyncSession
    ) -> UserModel:
        data = {
            "id": user_data.id,
            "username": user_data.username,
            "full_name": (
                user_data.first_name + (
                    " " + user_data.last_name
                    if user_data.last_name is not None
                    else ""
                )
            )
        }
        return await self.get_or_create(data, session)


class ChatManager(CRUDBase):
    """A class to manage users in a database."""

    async def add_chat(
        self,
        chat_data,
        session: AsyncSession
    ) -> UserModel:
        data = {
            "id": chat_data.id,
            "title": chat_data.title
        }
        return await self.get_or_create(data, session)


class MessageManager(CRUDBase):
    """A class to manage messages in a database."""

    async def add_message(
        self,
        message_data,
        session: AsyncSession
    ) -> MessageModel:
        data = {
            "id": message_data.id,
            "timestamp": message_data.date,
            "chat_id": abs(message_data.chat_id),
            "user_id": message_data.from_id.user_id,
        }
        return await self.get_or_create(data, session)


class ContentManager(CRUDBase):
    """A class to manage messages in a database."""

    async def add_content(
        self,
        message_data,
        session: AsyncSession
    ) -> MessageModel:
        data = {
            "timestamp": (
                message_data.edit_date
                if message_data.edit_date is not None
                else message_data.date
            ),
            "message_id": message_data.id,
            "text": message_data.text
        }
        instance = self.model(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


user_manager = UserManager(UserModel)
chat_manager = ChatManager(ChatModel)
message_manager = MessageManager(MessageModel)
content_manager = ContentManager(ContentModel)
