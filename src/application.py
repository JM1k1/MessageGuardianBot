
import asyncio

from dispatcher import bot, dp

from bot.handlers import group_router


async def main():
    dp.include_router(group_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
