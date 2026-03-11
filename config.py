"""
Конфигурационный файл для Telegram-бота по физике
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("⚠️  ВНИМАНИЕ: Токен не найден в файле .env")
    print("Создайте файл .env и добавьте строку: BOT_TOKEN=ваш_токен_здесь")
    TOKEN = input("Или введите токен сейчас: ").strip()