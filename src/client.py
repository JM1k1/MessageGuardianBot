from telethon import TelegramClient
from bot.core.settings import settings

client = TelegramClient(
    'MessageGuardian',
    settings.telegram_api_id,
    settings.telegram_api_hash
)
