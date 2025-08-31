#!/bin/bash

echo "🚀 Развертывание обновлений бота на сервере 164.90.237.57"
echo "=================================================="

# Проверяем подключение к серверу
echo "🔍 Проверяем подключение к серверу..."
if ! ping -c 1 164.90.237.57 &> /dev/null; then
    echo "❌ Сервер недоступен. Проверьте подключение к интернету."
    exit 1
fi

echo "✅ Сервер доступен"

# Подключаемся к серверу и выполняем обновления
echo "📡 Подключаемся к серверу и обновляем бота..."

ssh root@164.90.237.57 << 'EOF'

echo "🔄 Начинаем обновление бота..."

# Переходим в директорию бота
cd /root/spelling-check-bot

# Останавливаем бота
echo "⏹️ Останавливаем бота..."
sudo systemctl stop spelling-bot.service

# Создаем резервные копии
echo "💾 Создаем резервные копии..."
cp bot.py bot.py.backup.$(date +%Y%m%d_%H%M%S)
cp user_manager.py user_manager.py.backup.$(date +%Y%m%d_%H%M%S)

# Создаем новый файл telegram_utils.py
echo "📝 Создаем telegram_utils.py..."
cat > telegram_utils.py << 'TELEGRAM_UTILS'
import re
from typing import Tuple, Dict, Any
from telegram import Update, MessageEntity

class TelegramFormatter:
    """Утилиты для работы с форматированием Telegram сообщений"""
    
    @staticmethod
    def extract_text_and_entities(message) -> Tuple[str, list]:
        """Извлекает текст и сущности из сообщения"""
        text = message.text or ""
        entities = message.entities or []
        return text, entities
    
    @staticmethod
    def preserve_formatting(text: str, entities: list) -> str:
        """Сохраняет форматирование Telegram в тексте"""
        if not entities:
            return text
        
        # Сортируем сущности по позиции
        sorted_entities = sorted(entities, key=lambda x: x.offset)
        
        # Создаем маски форматирования
        formatting_map = {}
        
        for entity in sorted_entities:
            start = entity.offset
            end = entity.offset + entity.length
            
            # Определяем тип форматирования
            if entity.type == MessageEntity.BOLD:
                formatting_map[start] = "**"
                formatting_map[end] = "**"
            elif entity.type == MessageEntity.ITALIC:
                formatting_map[start] = "*"
                formatting_map[end] = "*"
            elif entity.type == MessageEntity.CODE:
                formatting_map[start] = "`"
                formatting_map[end] = "`"
            elif entity.type == MessageEntity.PRE:
                formatting_map[start] = "```\n"
                formatting_map[end] = "\n```"
            elif entity.type == MessageEntity.URL:
                # Сохраняем URL как есть
                continue
            elif entity.type == MessageEntity.TEXT_LINK:
                # Сохраняем ссылку в формате Markdown
                url = entity.url
                link_text = text[start:end]
                formatting_map[start] = f"[{link_text}]({url})"
                formatting_map[end] = ""
        
        # Применяем форматирование
        result = ""
        last_pos = 0
        
        for pos in sorted(formatting_map.keys()):
            result += text[last_pos:pos]
            result += formatting_map[pos]
            last_pos = pos
        
        result += text[last_pos:]
        
        return result
    
    @staticmethod
    def clean_formatting_for_llm(text: str) -> str:
        """Очищает текст от форматирования для отправки в LLM"""
        # Убираем Markdown форматирование
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Жирный
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Курсив
        text = re.sub(r'`(.*?)`', r'\1', text)        # Код
        text = re.sub(r'```(.*?)```', r'\1', text, flags=re.DOTALL)  # Блок кода
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Ссылки
        
        return text.strip()
    
    @staticmethod
    def format_result_message(original_text: str, result_text: str, operation: str) -> str:
        """Форматирует результат для отправки"""
        operation_emoji = {
            "check": "✅",
            "improve": "✨", 
            "shorten": "📄",
            "translate": "🌐"
        }
        
        emoji = operation_emoji.get(operation, "📝")
        
        # Если результат слишком длинный, разбиваем на части
        if len(result_text) > 4000:
            return f"{emoji} **Результат слишком длинный. Отправляю частями:**"
        
        return f"{emoji} **Результат:**\n\n{result_text}"
    
    @staticmethod
    def split_long_message(text: str, max_length: int = 4000) -> list:
        """Разбивает длинное сообщение на части"""
        if len(text) <= max_length:
            return [text]
        
        parts = []
        current_part = ""
        
        # Разбиваем по абзацам
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_part) + len(paragraph) + 2 <= max_length:
                current_part += (paragraph + '\n\n')
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = paragraph + '\n\n'
        
        if current_part:
            parts.append(current_part.strip())
        
        return parts
TELEGRAM_UTILS

echo "✅ telegram_utils.py создан"

# Перезапускаем бота
echo "▶️ Запускаем бота..."
sudo systemctl start spelling-bot.service

# Проверяем статус
echo "📊 Проверяем статус..."
sudo systemctl status spelling-bot.service

echo "✅ Обновление завершено!"
echo "📋 Для просмотра логов используйте: sudo journalctl -u spelling-bot.service -f"

EOF

echo "🎉 Развертывание завершено!"
echo "📱 Теперь бот поддерживает:"
echo "   ✅ Пересланные сообщения"
echo "   ✅ Отдельные сообщения с результатами"
echo "   ✅ Сохранение форматирования Telegram"
echo "   ✅ Разбивку длинных сообщений"
echo "   ✅ Исправленную команду /stats"
