import asyncio
import json
import os
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.methods import SendMessage, DeleteWebhook
from aiogram.types import Message
from dotenv import load_dotenv

from generate_output import generate_response

load_dotenv()

token = os.getenv('token')
# Set up the dispatcher
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    await message.answer('Hello, send your request as follows: {"dt_from": "2022-09-01T00:00:00", "dt_upto": '
                         '"2022-12-31T23:59:00", "group_type": "month"}')


@dp.message()
async def message_handler(message: types.Message) -> Optional[SendMessage]:
    json_ = json.loads(message.text)
    answer = generate_response(json_)
    return message.answer(str(answer))


async def main() -> None:
    bot = Bot(token)
    print('Started...')
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
