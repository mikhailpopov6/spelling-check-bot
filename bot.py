import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import TELEGRAM_TOKEN
from llm_service import LLMService
from user_manager import UserManager
from telegram_utils import TelegramFormatter

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TextBot:
    def __init__(self):
        self.llm_service = LLMService()
        self.user_manager = UserManager()
        self.user_states = {}  # Для отслеживания состояния пользователей
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        # Регистрируем пользователя
        user = update.effective_user
        self.user_manager.get_or_create_user(
            user.id, 
            user.username, 
            user.first_name
        )
        
        welcome_text = """
🤖 Добро пожаловать в бота для работы с русскими текстами!

Я помогу вам:
✅ Проверить грамотность текста
✅ Улучшить написание текста  
✅ Сократить текст с сохранением смысла
✅ Перевести текст на другие языки

Команды:
/check [текст] - проверить грамотность
/improve [текст] - улучшить текст
/shorten [текст] - сократить текст
/translate [язык] [текст] - перевести текст (en/uz/am/ru)
/help - справка

💡 К любой команде можно добавить nodot для удаления точек в конце абзацев

Выберите действие или отправьте текст для обработки:
        """
        
        keyboard = [
            [InlineKeyboardButton("📝 Проверить грамотность", callback_data="check_grammar")],
            [InlineKeyboardButton("✨ Улучшить текст", callback_data="improve_text")],
            [InlineKeyboardButton("📄 Сократить текст", callback_data="shorten_text")],
            [InlineKeyboardButton("🌐 Перевод", callback_data="translate")],
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

4️⃣ **Перевод** - переводит текст на английский, узбекский, армянский языки и с любого языка на русский

**Команды:**
/start - Главное меню
/help - Эта справка
/check [текст] - Проверить грамотность
/check [текст] nodot - Проверить грамотность без точек в конце абзацев
/improve [текст] - Улучшить текст  
/improve [текст] nodot - Улучшить текст без точек в конце абзацев
/shorten [текст] - Сократить текст
/shorten [текст] nodot - Сократить текст без точек в конце абзацев
/translate [язык] [текст] - Перевести текст (en/uz/am)
/translate [язык] [текст] nodot - Перевести текст без точек в конце абзацев

**Как использовать:**
1. Выберите действие через кнопки или команды
2. Отправьте текст для обработки (или сразу после команды)
3. Получите результат!

**Особенности:**
✅ Поддерживает многострочный текст с абзацами
✅ Сохраняет структуру форматирования
✅ Автоматически исправляет тире

**Примеры:**
/check Привет как дела
/check Привет как дела nodot
/improve Текст с ошибками
/improve Текст с ошибками nodot
/shorten Очень длинный текст который нужно сократить
/shorten Очень длинный текст который нужно сократить nodot
/translate en Привет мир
/translate uz Как дела
/translate am Добрый день

Максимальная длина текста: 4000 символов
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /check"""
        user_id = update.effective_user.id
        
        # Проверяем пересланное сообщение
        if update.message.forward_from or update.message.forward_from_chat:
            # Если это пересланное сообщение, берем текст из него
            text = update.message.text or ""
            if text.startswith('/check'):
                text = text[7:].strip()  # Убираем '/check '
        else:
            # Проверяем, есть ли текст после команды
            if context.args:
                # Получаем полный текст сообщения и убираем команду
                full_text = update.message.text
                command_length = len('/check')
                text = full_text[command_length:].strip()
            else:
                text = ""
        
        # Проверяем параметр nodot
        no_dot = 'nodot' in text.lower()
        if no_dot:
            # Убираем nodot из текста
            text = text.replace('nodot', '').replace('NODOT', '').strip()
        
        # Обрабатываем многострочные сообщения
        if text:
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            await self.process_check_text(update, text, no_dot)
        else:
            self.user_states[user_id] = "waiting_for_text_check"
            await update.message.reply_text("📝 Отправьте текст для проверки грамотности:")
    
    async def improve_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /improve"""
        user_id = update.effective_user.id
        
        # Проверяем пересланное сообщение
        if update.message.forward_from or update.message.forward_from_chat:
            # Если это пересланное сообщение, берем текст из него
            text = update.message.text or ""
            if text.startswith('/improve'):
                text = text[10:].strip()  # Убираем '/improve '
        else:
            # Проверяем, есть ли текст после команды
            if context.args:
                # Получаем полный текст сообщения и убираем команду
                full_text = update.message.text
                command_length = len('/improve')
                text = full_text[command_length:].strip()
            else:
                text = ""
        
        # Проверяем параметр nodot
        no_dot = 'nodot' in text.lower()
        if no_dot:
            # Убираем nodot из текста
            text = text.replace('nodot', '').replace('NODOT', '').strip()
        
        # Обрабатываем многострочные сообщения
        if text:
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            await self.process_improve_text(update, text, no_dot)
        else:
            self.user_states[user_id] = "waiting_for_text_improve"
            await update.message.reply_text("✨ Отправьте текст для улучшения:")
    
    async def shorten_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /shorten"""
        user_id = update.effective_user.id
        
        # Проверяем пересланное сообщение
        if update.message.forward_from or update.message.forward_from_chat:
            # Если это пересланное сообщение, берем текст из него
            text = update.message.text or ""
            if text.startswith('/shorten'):
                text = text[9:].strip()  # Убираем '/shorten '
        else:
            # Проверяем, есть ли текст после команды
            if context.args:
                # Получаем полный текст сообщения и убираем команду
                full_text = update.message.text
                command_length = len('/shorten')
                text = full_text[command_length:].strip()
            else:
                text = ""
        
        # Проверяем параметр nodot
        no_dot = 'nodot' in text.lower()
        if no_dot:
            # Убираем nodot из текста
            text = text.replace('nodot', '').replace('NODOT', '').strip()
        
        # Обрабатываем многострочные сообщения
        if text:
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            await self.process_shorten_text(update, text, no_dot)
        else:
            self.user_states[user_id] = "waiting_for_text_shorten"
            await update.message.reply_text("📄 Отправьте текст для сокращения:")
    
    async def translate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /translate"""
        user_id = update.effective_user.id
        
        # Проверяем пересланное сообщение
        if update.message.forward_from or update.message.forward_from_chat:
            # Если это пересланное сообщение, берем текст из него
            full_text = update.message.text or ""
            if full_text.startswith('/translate'):
                # Убираем '/translate ' и разбираем аргументы
                args_text = full_text[11:].strip()
                args = args_text.split()
                if len(args) >= 2:
                    target_language = args[0].lower()
                    text = ' '.join(args[1:])
                else:
                    text = ""
                    target_language = ""
            else:
                text = ""
                target_language = ""
        else:
            # Проверяем, есть ли аргументы после команды
            if len(context.args) >= 2:
                # Первый аргумент - язык, остальное - текст
                target_language = context.args[0].lower()
                text = ' '.join(context.args[1:])
            else:
                text = ""
                target_language = ""
        
        # Проверяем параметр nodot
        no_dot = 'nodot' in text.lower()
        if no_dot:
            # Убираем nodot из текста
            text = text.replace('nodot', '').replace('NODOT', '').strip()
        
        # Обрабатываем многострочные сообщения
        if text and target_language:
            text = text.replace('\r\n', '\n').replace('\r', '\n')
            await self.process_translate_text(update, text, target_language, no_dot)
        else:
            self.user_states[user_id] = "waiting_for_text_translate"
            await update.message.reply_text("🌐 Отправьте текст для перевода (укажите язык: en/uz/am/ru):")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats (только для админов)"""
        try:
            user_id = update.effective_user.id
            
            if not self.user_manager.is_admin(user_id):
                await update.message.reply_text("❌ У вас нет доступа к этой команде.")
                return
            
            stats = self.user_manager.get_stats()
            
            stats_text = f"""
📊 **Статистика бота**

👥 **Пользователи:**
• Всего пользователей: {stats.get('total_users', 0)}

📈 **Запросы:**
• Всего запросов: {stats.get('total_requests', 0)}
• За сегодня: {stats.get('today_requests', 0)}
• За неделю: {stats.get('week_requests', 0)}

🏆 **Топ-5 пользователей:**
"""
            
            top_users = stats.get('top_users', [])
            if top_users:
                for i, user in enumerate(top_users, 1):
                    username = user.get('username', 'Без username')
                    first_name = user.get('first_name', 'Неизвестно')
                    total_requests = user.get('requests', {}).get('total', 0)
                    stats_text += f"{i}. @{username} ({first_name}) - {total_requests} запросов\n"
            else:
                stats_text += "Пока нет данных о пользователях\n"
            
            await update.message.reply_text(stats_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Ошибка в команде stats: {e}")
            await update.message.reply_text("❌ Произошла ошибка при получении статистики. Проверьте логи.")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        # Обработка пересланных сообщений
        if query.data.startswith("forward_"):
            action = query.data.split("_")[1]
            
            # Получаем сохраненный текст
            if user_id in self.user_states and self.user_states[user_id].startswith("forwarded_text:"):
                text = self.user_states[user_id].replace("forwarded_text:", "")
                
                if action == "check":
                    await self.process_check_text(update, text, False)
                elif action == "improve":
                    await self.process_improve_text(update, text, False)
                elif action == "shorten":
                    await self.process_shorten_text(update, text, False)
                elif action == "translate":
                    await query.edit_message_text("🌐 Для перевода используйте команду:\n\n/translate [язык] [текст]\n\nПоддерживаемые языки:\n• en - английский\n• uz - узбекский\n• am - армянский\n• ru - русский (автоопределение языка)\n\nПримеры:\n/translate en Привет мир\n/translate ru Hello world")
                
                # Очищаем состояние
                if user_id in self.user_states:
                    del self.user_states[user_id]
                return
        
        # Обычные кнопки
        if query.data == "check_grammar":
            self.user_states[user_id] = "waiting_for_text_check"
            await query.edit_message_text("📝 Отправьте текст для проверки грамотности:")
        
        elif query.data == "improve_text":
            self.user_states[user_id] = "waiting_for_text_improve"
            await query.edit_message_text("✨ Отправьте текст для улучшения:")
        
        elif query.data == "shorten_text":
            self.user_states[user_id] = "waiting_for_text_shorten"
            await query.edit_message_text("📄 Отправьте текст для сокращения:")
        
        elif query.data == "translate":
            await query.edit_message_text("🌐 Для перевода используйте команду:\n\n/translate [язык] [текст]\n\nПоддерживаемые языки:\n• en - английский\n• uz - узбекский\n• am - армянский\n• ru - русский (автоопределение языка)\n\nПримеры:\n/translate en Привет мир\n/translate ru Hello world\n/translate uz Как дела\n/translate ru Salom dunyo")
        
        elif query.data == "help":
            help_text = """
📚 **Как использовать бота:**

1️⃣ **Проверить грамотность** - исправляет орфографические и пунктуационные ошибки, сохраняя стиль текста

2️⃣ **Улучшить текст** - исправляет ошибки и улучшает стиль, делая текст более читаемым

3️⃣ **Сократить текст** - убирает лишние слова, сохраняя основную мысль и грамотность

4️⃣ **Перевод** - переводит текст на английский, узбекский, армянский языки и с любого языка на русский

**Команды:**
/start - Главное меню
/help - Эта справка
/check [текст] - Проверить грамотность
/check [текст] nodot - Проверить грамотность без точек в конце абзацев
/improve [текст] - Улучшить текст  
/improve [текст] nodot - Улучшить текст без точек в конце абзацев
/shorten [текст] - Сократить текст
/shorten [текст] nodot - Сократить текст без точек в конце абзацев
/translate [язык] [текст] - Перевести текст (en/uz/am/ru)
/translate [язык] [текст] nodot - Перевести текст без точек в конце абзацев

**Как использовать:**
1. Выберите действие через кнопки или команды
2. Отправьте текст для обработки (или сразу после команды)
3. Получите результат!

**Примеры:**
/check Привет как дела
/check Привет как дела nodot
/improve Текст с ошибками
/improve Текст с ошибками nodot
/shorten Очень длинный текст который нужно сократить
/shorten Очень длинный текст который нужно сократить nodot
/translate en Привет мир
/translate ru Hello world
/translate uz Как дела
/translate ru Salom dunyo

Максимальная длина текста: 4000 символов
            """
            await query.edit_message_text(help_text, parse_mode='Markdown')
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_id = update.effective_user.id
        message = update.message
        
        # Извлекаем текст и форматирование
        text, entities = TelegramFormatter.extract_text_and_entities(message)
        
        # Обрабатываем многострочные сообщения
        if text and '\n' in text:
            # Нормализуем переносы строк
            text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        if user_id not in self.user_states:
            # Если пользователь не в состоянии ожидания, показываем главное меню
            await self.start(update, context)
            return
        
        state = self.user_states[user_id]
        
        # Отправляем сообщение о начале обработки
        processing_msg = await update.message.reply_text("🔄 Обрабатываю текст...")
        
        try:
            # Очищаем текст от форматирования для LLM
            clean_text = TelegramFormatter.clean_formatting_for_llm(text)
            
            if state == "waiting_for_text_check":
                # Записываем запрос
                self.user_manager.record_request(user_id, "check_grammar")
                result = await self.llm_service.check_grammar(clean_text)
                await self.send_result_message(update, result, "check", processing_msg)
            
            elif state == "waiting_for_text_improve":
                # Записываем запрос
                self.user_manager.record_request(user_id, "improve_text")
                result = await self.llm_service.improve_text(clean_text)
                await self.send_result_message(update, result, "improve", processing_msg)
            
            elif state == "waiting_for_text_shorten":
                # Записываем запрос
                self.user_manager.record_request(user_id, "shorten_text")
                result = await self.llm_service.shorten_text(clean_text)
                await self.send_result_message(update, result, "shorten", processing_msg)
            
            elif state == "waiting_for_text_translate":
                # Записываем запрос
                self.user_manager.record_request(user_id, "translate_text")
                # Показываем инструкцию для перевода
                await processing_msg.edit_text("🌐 Для перевода используйте команду:\n/translate [язык] [текст]\n\nПоддерживаемые языки:\n• en - английский\n• uz - узбекский\n• am - армянский\n• ru - русский (автоопределение языка)\n\nПримеры:\n/translate en Привет мир\n/translate ru Hello world")
        
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при обработке текста: {e}")
        
        finally:
            # Очищаем состояние пользователя
            if user_id in self.user_states:
                del self.user_states[user_id]
    
    async def send_result_message(self, update: Update, result: str, operation: str, processing_msg=None):
        """Отправляет результат отдельным сообщением"""
        try:
            # Удаляем сообщение о обработке
            if processing_msg:
                await processing_msg.delete()
            
            # Разбиваем длинное сообщение на части
            parts = TelegramFormatter.split_long_message(result)
            
            if len(parts) == 1:
                # Отправляем одно сообщение
                await update.message.reply_text(result, parse_mode='Markdown')
            else:
                # Отправляем несколько частей
                for i, part in enumerate(parts, 1):
                    if i == 1:
                        await update.message.reply_text(f"📄 **Часть {i}/{len(parts)}:**\n\n{part}", parse_mode='Markdown')
                    else:
                        await update.message.reply_text(f"📄 **Часть {i}/{len(parts)}:**\n\n{part}", parse_mode='Markdown')
        
        except Exception as e:
            logger.error(f"Ошибка при отправке результата: {e}")
            await update.message.reply_text(f"❌ Ошибка при отправке результата: {str(e)}")
    
    async def handle_forwarded_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик пересланных сообщений"""
        user_id = update.effective_user.id
        message = update.message
        
        # Извлекаем текст и форматирование
        text, entities = TelegramFormatter.extract_text_and_entities(message)
        
        # Обрабатываем многострочные сообщения
        if text and '\n' in text:
            text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        if not text:
            await update.message.reply_text("❌ Пересланное сообщение не содержит текста.")
            return
        
        # Показываем меню выбора действия
        keyboard = [
            [InlineKeyboardButton("📝 Проверить грамотность", callback_data=f"forward_check:{text[:50]}...")],
            [InlineKeyboardButton("✨ Улучшить текст", callback_data=f"forward_improve:{text[:50]}...")],
            [InlineKeyboardButton("📄 Сократить текст", callback_data=f"forward_shorten:{text[:50]}...")],
            [InlineKeyboardButton("🌐 Перевод", callback_data=f"forward_translate:{text[:50]}...")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📤 **Пересланное сообщение:**\n\n{text[:200]}{'...' if len(text) > 200 else ''}\n\nВыберите действие:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Сохраняем полный текст для обработки
        self.user_states[user_id] = f"forwarded_text:{text}"
    
    async def process_check_text(self, update: Update, text: str, no_dot: bool = False):
        """Обрабатывает текст для проверки грамотности"""
        user_id = update.effective_user.id
        
        # Записываем запрос
        self.user_manager.record_request(user_id, "check_grammar")
        
        processing_msg = await update.message.reply_text("🔄 Проверяю грамотность...")
        try:
            result = await self.llm_service.check_grammar(text, no_dot)
            await self.send_result_message(update, result, "check", processing_msg)
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при проверке грамотности: {e}")
    
    async def process_improve_text(self, update: Update, text: str, no_dot: bool = False):
        """Обрабатывает текст для улучшения"""
        user_id = update.effective_user.id
        
        # Записываем запрос
        self.user_manager.record_request(user_id, "improve_text")
        
        processing_msg = await update.message.reply_text("🔄 Улучшаю текст...")
        try:
            result = await self.llm_service.improve_text(text, no_dot)
            await self.send_result_message(update, result, "improve", processing_msg)
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при улучшении текста: {e}")
    
    async def process_shorten_text(self, update: Update, text: str, no_dot: bool = False):
        """Обрабатывает текст для сокращения"""
        user_id = update.effective_user.id
        
        # Записываем запрос
        self.user_manager.record_request(user_id, "shorten_text")
        
        processing_msg = await update.message.reply_text("🔄 Сокращаю текст...")
        try:
            result = await self.llm_service.shorten_text(text, no_dot)
            await self.send_result_message(update, result, "shorten", processing_msg)
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при сокращении текста: {e}")
    
    async def process_translate_text(self, update: Update, text: str, target_language: str, no_dot: bool = False):
        """Обрабатывает текст для перевода"""
        user_id = update.effective_user.id
        
        # Записываем запрос
        self.user_manager.record_request(user_id, "translate_text")
        
        # Определяем название языка для отображения
        language_names = {
            "en": "английский",
            "uz": "узбекский", 
            "am": "армянский",
            "ru": "русский"
        }
        language_name = language_names.get(target_language, target_language)
        
        # Определяем направление перевода
        if target_language == "ru":
            direction = "на русский"
            processing_text = "🌐 Перевожу на русский..."
            result_text = f"🌐 **Перевод на русский:**"
        else:
            direction = f"на {language_name}"
            processing_text = f"🌐 Перевожу {direction}..."
            result_text = f"🌐 **Перевод {direction}:**"
        
        processing_msg = await update.message.reply_text(processing_text)
        try:
            result = await self.llm_service.translate_text(text, target_language, no_dot)
            await processing_msg.edit_text(f"{result_text}\n\n{result}", parse_mode='Markdown')
        except Exception as e:
            await processing_msg.edit_text(f"❌ Произошла ошибка: {str(e)}")
            logger.error(f"Ошибка при переводе текста: {e}")
    
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
    application.add_handler(CommandHandler("translate", bot.translate_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    
    # Обработчики для кнопок и текста
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_text))
    
    # Обработчик пересланных сообщений
    application.add_handler(MessageHandler(filters.FORWARDED & filters.TEXT, bot.handle_forwarded_message))
    
    # Обработчик ошибок
    application.add_error_handler(bot.error_handler)
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 