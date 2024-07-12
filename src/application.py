import asyncio

from dispatcher import bot, dp

from bot.database.database import create_table
from bot.handlers import group_router


async def main():
    await create_table()
    dp.include_router(group_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
