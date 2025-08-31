#!/bin/bash

echo "🔄 Обновление бота на сервере..."

# Переходим в директорию бота
cd /root/spelling-check-bot

# Останавливаем бота
echo "⏹️ Останавливаем бота..."
sudo systemctl stop spelling-bot.service

# Создаем резервную копию
echo "💾 Создаем резервную копию..."
cp bot.py bot.py.backup
cp user_manager.py user_manager.py.backup

# Обновляем файлы
echo "📝 Обновляем файлы..."

# Копируем обновленные файлы (замените на ваши пути)
# cp /path/to/updated/bot.py .
# cp /path/to/updated/user_manager.py .
# cp /path/to/updated/telegram_utils.py .

echo "📋 Обновленные файлы:"
echo "- bot.py (улучшенная обработка сообщений)"
echo "- user_manager.py (исправлена команда stats)"
echo "- telegram_utils.py (новый файл для форматирования)"

# Перезапускаем бота
echo "▶️ Запускаем бота..."
sudo systemctl start spelling-bot.service

# Проверяем статус
echo "📊 Проверяем статус..."
sudo systemctl status spelling-bot.service

echo "✅ Обновление завершено!"
echo "📋 Для просмотра логов используйте: sudo journalctl -u spelling-bot.service -f"
