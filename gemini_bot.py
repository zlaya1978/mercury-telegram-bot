import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Инициализация
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not GEMINI_API_KEY:
    raise ValueError('GEMINI_API_KEY not found in environment')
if not TELEGRAM_TOKEN:
    raise ValueError('TELEGRAM_BOT_TOKEN not found in environment')

genai.configure(api_key=GEMINI_API_KEY)

# Инициализация модели Gemini
model = genai.GenerativeModel('gemini-pro')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящих сообщений"""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Показать что бот печатает
    await update.message.chat.send_action('typing')
    
    try:
        # Система промпт для агента по недвижимости
        system_prompt = """Ты помощник по недвижимости для агентства Mercury. 
Отвечай профессионально и кратко на вопросы о недвижимости, ипотеке, аренде и покупке квартир.
Если пользователь хочет оставить свои контакты - предложи сохранить их для связи."""
        
        # Генерируем ответ от Gemini
        response = model.generate_content(f"{system_prompt}\n\nПользователь: {user_message}")
        ai_response = response.text
        
        # Отправляем ответ
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        error_msg = f"Извините, произошла ошибка: {str(e)}"
        await update.message.reply_text(error_msg)
        print(f"Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start"""
    welcome_msg = """Добро пожаловать в Mercury Real Estate Bot! 🏠
    
Я помогу вам найти идеальную квартиру или дом.

Что вас интересует?
- Покупка квартиры
- Аренда жилья
- Информация об ипотеке
- Консультация агента

Просто напишите ваш вопрос!"""
    await update.message.reply_text(welcome_msg)

async def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(MessageHandler(filters.COMMAND & filters.TEXT, start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Бот запущен и ждёт сообщений...")
    print(f"Используется Gemini API для ответов")
    
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
