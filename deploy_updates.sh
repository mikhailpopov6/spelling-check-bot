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

# Копируем обновленные файлы на сервер
echo "📤 Копируем обновленные файлы на сервер..."

# Создаем временную директорию на сервере
ssh root@164.90.237.57 "mkdir -p /tmp/bot-update"

# Копируем файлы
scp bot.py root@164.90.237.57:/tmp/bot-update/
scp user_manager.py root@164.90.237.57:/tmp/bot-update/
scp telegram_utils.py root@164.90.237.57:/tmp/bot-update/
scp NEW_FEATURES.md root@164.90.237.57:/tmp/bot-update/

echo "✅ Файлы скопированы"

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

# Копируем обновленные файлы
echo "📝 Копируем обновленные файлы..."
cp /tmp/bot-update/bot.py .
cp /tmp/bot-update/user_manager.py .
cp /tmp/bot-update/telegram_utils.py .
cp /tmp/bot-update/NEW_FEATURES.md .

# Очищаем временную директорию
rm -rf /tmp/bot-update

echo "✅ Файлы обновлены"

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
