import datetime

from dispatcher import bot

from aiogram import Router
from aiogram.types import Message

from bot.core.settings import settings
from bot.database.crud import content_manager, message_manager, user_manager
from bot.database.database import async_session
from bot.filters import ChatTypeFilter


LOCAL_TIMEZONE = datetime.timezone(datetime.timedelta(hours=6))
DATETIME_FORMAT = "%H:%M %d.%m.%Y"

group_router = Router()
group_router.message.filter(
    ChatTypeFilter(chat_type=["group", "supergroup"])
)


@group_router.message()
async def group_message_handler(message: Message):
    user_data = message.from_user
    if not message.text or user_data.is_bot:
        return

    await bot.forward_message(
        settings.forward_chat_id,
        message.chat.id,
        message.message_id
    )

    async with async_session() as session:
        await user_manager.add_user(user_data, session)
        await message_manager.add_message(message, session)
        await content_manager.add_content(message, session)


@group_router.edited_message()
async def group_edited_message_handler(message: Message):
    async with async_session() as session:
        await content_manager.add_content(message, session)

        await bot.forward_message(
            settings.forward_chat_id,
            message.chat.id,
            message.message_id
        )

        msg = await message_manager.get(message.message_id, session)
        await session.refresh(msg, attribute_names=["contents"])
        print(message.from_user.full_name + " \n" +
              "\n|-> ".join(f"{content.text} [{content.timestamp.astimezone(LOCAL_TIMEZONE).strftime(format)}]" for content in msg.contents))
