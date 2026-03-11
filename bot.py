import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (это для локального теста)
load_dotenv()
# А на сервере токен будет просто храниться в переменных окружения
TOKEN = os.getenv('BOT_TOKEN')
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN
from knowledge_base import physics_knowledge, search_knowledge

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Клавиатура с основными разделами
main_keyboard = ReplyKeyboardMarkup([
    ['📚 Механика', '🧪 МКТ и Термодинамика'],
    ['🔍 Поиск', '❓ Помощь']
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        logger.info(f"Команда /start получена от пользователя {update.effective_user.id}")
        
        welcome_message = (
            "👋 **Привет! Я бот-помощник по физике для 10 класса!**\n\n"
            "Я помогу тебе разобраться с:\n"
            "• Законами Ньютона\n"
            "• Законами сохранения\n"
            "• Газовыми законами\n"
            "• МКТ и термодинамикой\n\n"
            "Выбери раздел на клавиатуре или просто напиши вопрос!"
        )
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='Markdown', 
            reply_markup=main_keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        await update.message.reply_text("Произошла ошибка при запуске. Попробуйте еще раз.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    try:
        help_text = (
            "🤔 **Как пользоваться ботом:**\n\n"
            "1️⃣ Выбери раздел на клавиатуре\n"
            "2️⃣ Напиши конкретный вопрос\n"
            "3️⃣ Используй режим поиска\n\n"
            "**Доступные команды:**\n"
            "/start - начать работу\n"
            "/help - показать эту справку\n"
            "/formulas - все формулы\n"
            "/laws - основные законы"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка в help: {e}")

async def formulas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать основные формулы"""
    try:
        formulas_text = (
            "📐 **Основные формулы:**\n\n"
            "**Законы Ньютона:**\n"
            "• II закон: F = ma\n"
            "• III закон: F₁₂ = -F₂₁\n\n"
            "**Закон всемирного тяготения:**\n"
            "• F = G(m₁m₂/R²)\n"
            "• F = mg (сила тяжести)\n\n"
            "**Законы сохранения:**\n"
            "• Импульс: p = mv\n"
            "• Энергия: Ек + Еп = const\n\n"
            "**Газовые законы:**\n"
            "• МКТ: P = (1/3)nm₀v²\n"
            "• Менделеев-Клапейрон: PV = νRT\n"
            "• Изотерма: PV = const\n"
            "• Изобара: V/T = const\n"
            "• Изохора: P/T = const\n\n"
            "**Термодинамика:**\n"
            "• I закон: Q = ∆U + A"
        )
        await update.message.reply_text(formulas_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Ошибка в formulas: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    try:
        text = update.message.text
        user = update.effective_user
        
        logger.info(f"Сообщение от {user.first_name}: {text}")
        
        # Обработка кнопок меню
        if text == '📚 Механика':
            response = (
                "**Механика**\n\n"
                "• Законы Ньютона\n"
                "• Закон всемирного тяготения\n"
                "• Законы сохранения\n"
                "• Закон Гука\n\n"
                "Напиши конкретный вопрос!"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
            
        elif text == '🧪 МКТ и Термодинамика':
            response = (
                "**МКТ и термодинамика**\n\n"
                "• Основное уравнение МКТ\n"
                "• Уравнение Менделеева-Клапейрона\n"
                "• Газовые законы\n"
                "• Первый закон термодинамики\n\n"
                "Напиши конкретный вопрос!"
            )
            await update.message.reply_text(response, parse_mode='Markdown')
            
        elif text == '🔍 Поиск':
            await update.message.reply_text(
                "Напиши ключевое слово для поиска\n"
                "Например: инерция, импульс, изотерма"
            )
            
        elif text == '❓ Помощь':
            await help_command(update, context)
            
        else:
            # Поиск по базе знаний
            results = search_knowledge(text)
            
            if results and results[0] != "К сожалению, информация по вашему запросу не найдена.":
                for result in results:
                    await update.message.reply_text(result, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "❌ Информация не найдена. Попробуй переформулировать вопрос.",
                    reply_markup=main_keyboard
                )
                
    except Exception as e:
        logger.error(f"Ошибка в handle_message: {e}")
        await update.message.reply_text("Произошла ошибка при обработке сообщения.")

def main():
    """Главная функция запуска бота"""
    try:
        # Проверка токена
        if not TOKEN:
            logger.error("Токен не найден!")
            print("❌ ОШИБКА: Токен не найден! Создайте файл .env с BOT_TOKEN=ваш_токен")
            return
        
        print(f"✅ Токен загружен: {TOKEN[:10]}...")
        
        # Создание приложения
        application = Application.builder().token(TOKEN).build()
        
        # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("formulas", formulas))
        application.add_handler(CommandHandler("laws", formulas))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запуск бота
        print("✅ Бот запускается...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        print(f"❌ Ошибка при запуске: {e}")
        print("\nВозможные решения:")
        print("1. Проверьте установку библиотеки: pip install python-telegram-bot==20.7")
        print("2. Проверьте токен в файле .env")
        print("3. Убедитесь, что интернет работает")

if __name__ == '__main__':
    main()