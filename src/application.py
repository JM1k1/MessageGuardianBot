from client import client

from telethon import events

from bot.core.settings import settings
from bot.handlers import (
    group_delited_message_handler,
    group_edited_message_handler,
    group_message_handler,
)


client.add_event_handler(group_message_handler, events.NewMessage)
client.add_event_handler(group_edited_message_handler, events.MessageEdited)
client.add_event_handler(group_delited_message_handler, events.MessageDeleted)


if __name__ == "__main__":
    client.start(bot_token=settings.telegram_token)
    client.run_until_disconnected()
