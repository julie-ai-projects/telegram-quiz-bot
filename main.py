from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json, sqlite3, asyncio

bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Welcome to the Quiz Bot! Type /quiz to begin 🎯")

@dp.message_handler(commands=["quiz"])
async def quiz(message: types.Message):
    await message.answer("Question 1: What is Python? 🐍")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
