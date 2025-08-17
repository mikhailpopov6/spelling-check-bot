#!/bin/bash

# Быстрый деплой бота на Digital Ocean
# Использование: ./quick-deploy.sh

set -e

echo "🚀 Быстрый деплой бота на Digital Ocean"
echo "========================================"

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Устанавливаем..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker установлен. Перезапустите терминал и попробуйте снова."
    exit 1
fi

# Проверяем наличие docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Создаем .env файл если его нет
if [ ! -f ".env" ]; then
    echo "📝 Создание файла .env..."
    cat > .env << EOF
# Telegram Bot Token
TELEGRAM_TOKEN=8475569974:AAF1MWVwTail48jAWkpkQfx4hLk6aX9c3aI

# Yandex Cloud API
YANDEX_API_KEY=AQVN18PYvPyNkfObkh7O9EWgcpXZzG47AEOc0lnU
YANDEX_FOLDER_ID=b1gvsm0staqq3jcivgl5
EOF
    echo "⚠️  Файл .env создан. Проверьте и отредактируйте ключи при необходимости."
fi

# Создаем директорию для логов
mkdir -p logs

# Собираем и запускаем контейнер
echo "🔨 Сборка и запуск контейнера..."
docker-compose up -d --build

echo "✅ Бот запущен!"
echo "📊 Статус: docker-compose ps"
echo "📋 Логи: docker-compose logs -f"
echo "🛑 Остановка: docker-compose down"
echo "🔄 Обновление: docker-compose pull && docker-compose up -d" 