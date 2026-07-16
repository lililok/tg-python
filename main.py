import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

###https://my.hip.hosting/

# 1. Загрузка настроек
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# --- НАСТРОЙКИ ---
# Сюда мы вставим ID картинки, когда получим его
PHOTO_ID = "" 

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- ХЭНДЛЕРЫ (ОБРАБОТЧИКИ) ---

# 2. Команда /start (Самая важная, ставим первой)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я бот-визитка. Пока я умею немного, но я быстро учусь.\n"
        "Нажми /help, чтобы узнать подробности."
    )

@dp.message(Command("photo"))
async def cmd_photo(message: types.Message):
    if PHOTO_ID == "":
        await message.answer("Сначала настройте PHOTO_ID в коде!")
        return
    
    # Отправляем фото по его ID (мгновенно)
    await message.answer_photo(photo=PHOTO_ID, caption="Вот твое фото! 🚀")


@dp.message(F.photo)
async def get_photo_id(message: types.Message):
    # Берем последнее фото (оно самого высокого качества)
    photo_data = message.photo[-1]
    file_id = photo_data.file_id
    
    await message.answer(
        f"✅ Фото получено!\n\n"
        f"Скопируй этот ID и вставь в переменную PHOTO_ID:\n"
        f"{file_id}"
    )

@dp.message(F.document)
async def warning_doc(message: types.Message):
    await message.answer(
        "⚠️ Ты прислал это как файл.\n"
        "Telegram не показывает превью для файлов.\n"
        "Пожалуйста, пришли именно как Фото (сжатое)."
    )

# 3. Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🤖 Справка:\n\n"
        "/start - Начать работу заново\n"
        "/help - Показать это сообщение\n"
        "/about - Об авторе\n\n"
        "Просто отправь мне любой текст, и я отвечу."
    )

@dp.message(Command("about"))
async def cmd_start(message: types.Message):
    await message.answer(
        "я бот <b>залупыш</b>\n"
        "создан <i>сонечкой ешану</i>\n"
        "<a href='https://vk.com/wall-202965685_3221'>лучшей айтишницей всея белогорья</a>\n\n"
        "а ты сдал инфу на сотку?"
    )

# 4. "Ловушка" для всех остальных сообщений
# (Ставим В САМОМ НИЗУ. Если поставить выше, команды сломаются!)
@dp.message()
async def echo_handler(message: types.Message):
    # Проверяем, что пользователь прислал именно текст, а не стикер/фото
    if message.text:
        await message.answer(f"Ты написал: {message.text}")
    else:
        await message.answer("Я понимаю только текст, извини 🤷‍♂️")

# --- ЗАПУСК ---
async def main():
    print("🚀 Бот запущен! (Нажми Ctrl+C для остановки)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
