import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN
from llm_service import LLMService

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TextBot:
    def __init__(self):
        self.llm_service = LLMService()
        self.user_states = {}  # Для отслеживания состояния пользователей
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🤖 Добро пожаловать в бота для работы с русскими текстами!

Я помогу вам:
✅ Проверить грамотность текста
✅ Улучшить написание текста  
✅ Сократить текст с сохранением смысла

Выберите действие или отправьте текст для обработки:
        """
        
        keyboard = [
            [InlineKeyboardButton("📝 Проверить грамотность", callback_data="check_grammar")],
            [InlineKeyboardButton("✨ Улучшить текст", callback_data="improve_text")],
            [InlineKeyboardButton("📄 Сократить текст", callback_data="shorten_text")],
            [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
📚 **Как использовать бота:**

1️⃣ **Проверить грамотность** - исправляет орфографические и пунктуационные ошибки, сохраняя стиль текста

2️⃣ **Улучшить текст** - исправляет ошибки и улучшает стиль, делая текст более читаемым

3️⃣ **Сократить текст** - убирает лишние слова, сохраняя основную мысль и грамотность

**Команды:**
/start - Главное меню
/help - Эта справка
/check - Проверить грамотность
/improve - Улучшить текст  
/shorten - Сократить текст

**Как использовать:**
1. Выберите действие
2. Отправьте текст для обработки
3. Получите результат!

Максимальная длина текста: 4000 символов
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /check"""
        user_id = update.effective_user.id
        self.user_states[user_id] = "waiting_for_text_check"
        await update.message.reply_text("📝 Отправьте текст для проверки грамотности:")
    
    async def improve_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /improve"""
        user_id = update.effective_user.id
        self.user_states[user_id] = "waiting_for_text_improve"
        await update.message.reply_text("✨ Отправьте текст для улучшения:")
    
    async def shorten_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /shorten"""
        user_id = update.effective_user.id
        self.user_states[user_id] = "waiting_for_text_shorten"
        await update.message.reply_text("📄 Отправьте текст для сокращения:")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == "check_grammar":
            self.user_states[user_id] = "waiting_for_text_check"
            await query.edit_message_text("📝 Отправьте текст для проверки грамотности:")
        
        elif query.data == "improve_text":
            self.user_states[user_id] = "waiting_for_text_improve"
            await query.edit_message_text("✨ Отправьте текст для улучшения:")
        
        elif query.data == "shorten_text":
            self.user_states[user_id] = "waiting_for_text_shorten"
            await query.edit_message_text("📄 Отправьте текст для сокращения:")
        
        elif query.data == "help":
            help_text = """
📚 **Как использовать бота:**

1️⃣ **Проверить грамотность** - исправляет орфографические и пунктуационные ошибки, сохраняя стиль текста

2️⃣ **Улучшить текст** - исправляет ошибки и улучшает стиль, делая текст более читаемым

3️⃣ **Сократить текст** - убирает лишние слова, сохраняя основную мысль и грамотность

**Команды:**
/start - Главное меню
/help - Эта справка
/check - Проверить грамотность
/improve - Улучшить текст  
/shorten - Сократить текст

**Как использовать:**
1. Выберите действие
2. Отправьте текст для обработки
3. Получите результат!

Максимальная длина текста: 4000 символов
            """
            await query.edit_message_text(help_text, parse_mode='Markdown')
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        text = update.message.text
        
        if user_id not in self.user_states:
            # Если пользователь не в состоянии ожидания, показываем главное меню
            await self.start(update, context)
            return
        
        state = self.user_states[user_id]
        
        # Отправляем сообщение о начале обработки
        processing_msg = await update.message.reply_text("🔄 Обрабатываю текст...")
        
        try:
            if state == "waiting_for_text_check":
                result = await self.llm_service.check_grammar(text)
                await processing_msg.edit_text(f"✅ **Результат проверки грамотности:**\n\n{result}", parse_mode='Markdown')
            
            elif state == "waiting_for_text_improve":
                result = await self.llm_service.improve_text(text)
                await processing_msg.edit_text(f"✨ **Улучшенный текст:**\n\n{result}", parse_mode='Markdown')
            
            elif state == "waiting_for_text_shorten":
                result = await self.llm_service.shorten_text(text)
                await processing_msg.edit_text(f"📄 **Сокращенный текст:**\n\n{result}", parse_mode='Markdown')
        
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при обработке текста: {e}")
        
        finally:
            # Очищаем состояние пользователя
            if user_id in self.user_states:
                del self.user_states[user_id]
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Ошибка: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text("❌ Произошла ошибка. Попробуйте позже.")

def main():
    """Основная функция запуска бота"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN не найден в переменных окружения")
        return
    
    # Создаем экземпляр бота
    bot = TextBot()
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("check", bot.check_command))
    application.add_handler(CommandHandler("improve", bot.improve_command))
    application.add_handler(CommandHandler("shorten", bot.shorten_command))
    
    # Обработчики для кнопок и текста
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_text))
    
    # Обработчик ошибок
    application.add_error_handler(bot.error_handler)
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 