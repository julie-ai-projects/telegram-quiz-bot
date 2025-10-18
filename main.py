import json
import random
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Load questions
with open("questions.json", "r") as f:
    QUESTIONS = json.load(f)

# Database setup
conn = sqlite3.connect("quiz.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, score INTEGER DEFAULT 0)")
conn.commit()

# Helper functions
def get_question():
    return random.choice(QUESTIONS)

def get_score(user_id):
    cur.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else 0

def update_score(user_id, increment):
    cur.execute("INSERT OR IGNORE INTO users (user_id, score) VALUES (?, 0)", (user_id,))
    cur.execute("UPDATE users SET score = score + ? WHERE user_id=?", (increment, user_id))
    conn.commit()

# Start command
@dp.message_handler(commands=["start"])
async def start_quiz(message: types.Message):
    await message.answer("👋 Hello! Welcome to the Quiz Bot!\nType /quiz to start playing 🎯")

# Quiz command
@dp.message_handler(commands=["quiz"])
async def send_question(message: types.Message):
    question = get_question()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for option in question["options"]:
        markup.add(option)
    await message.answer(question["question"], reply_markup=markup)

    # Save question in user data
    dp.current_state(user=message.from_user.id).update_data(current_question=question)

# Handle answers
@dp.message_handler(lambda msg: True)
async def check_answer(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    data = await state.get_data()
    question = data.get("current_question")

    if not question:
        return await message.answer("Type /quiz to start a new game 🎯")

    if message.text == question["answer"]:
        update_score(message.from_user.id, 1)
        await message.answer("✅ Correct! 🎉", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(f"❌ Wrong! The correct answer was: {question['answer']}", reply_markup=types.ReplyKeyboardRemove())

    score = get_score(message.from_user.id)
    await message.answer(f"Your current score: {score} 🧠\nType /quiz for another question!")

    await state.reset_data()

if __name__ == "__main__":
    print("Bot is running...")
    executor.start_polling(dp, skip_updates=True)
