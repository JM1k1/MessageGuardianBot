import datetime

from client import client

from bot.core.settings import settings
from bot.database.crud import (
    chat_manager,
    content_manager,
    message_manager,
    user_manager,
)
from bot.database.database import async_session


LOCAL_TIMEZONE = datetime.timezone(datetime.timedelta(hours=6))
DATETIME_FORMAT = "%H:%M %d.%m.%y"


async def group_message_handler(message):
    if not message.is_group or not message.text:
        return

    user_data = await client.get_entity(message.from_id.user_id)
    chat_data = await client.get_entity(message.chat_id)

    if user_data.bot:
        return

    async with async_session() as session:
        await user_manager.add_user(user_data, session)
        await chat_manager.add_chat(chat_data, session)
        await message_manager.add_message(message, session)
        await content_manager.add_content(message, session)


async def group_edited_message_handler(message):
    if not message.is_group or not message.text:
        return

    async with async_session() as session:
        await content_manager.add_content(message, session)


async def group_delited_message_handler(event):
    async with async_session() as session:
        for message_id in event.deleted_ids:
            message = await message_manager.get(message_id, session)

            if not message:
                return

            await session.refresh(message, attribute_names=[
                "contents", "chat", "user"
            ])

            contents = [
                [
                    content.text,
                    content.timestamp.astimezone(
                        LOCAL_TIMEZONE
                    ).strftime(DATETIME_FORMAT)
                ]
                for content in message.contents
            ]

            text = (
                f"**[{message.user.full_name}](@{message.user.username})** "
                f"** ⟵ Удалил cообщение в чате "
                f"__{message.chat.title}__:**\n\n" +
                "\n".join(
                    f"{text}\n`{date}`\n"
                    for text, date in contents
                )
            )

            await client.send_message(message.chat.id, text)
            await client.send_message(settings.forward_chat_id, text)

            message.deleted = True
            await session.commit()
