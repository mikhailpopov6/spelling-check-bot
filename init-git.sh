#!/bin/bash

# Скрипт для инициализации git репозитория
# Использование: ./init-git.sh

set -e

echo "🔧 Инициализация Git репозитория"
echo "================================"

# Проверяем, что мы в правильной директории
if [ ! -f "bot.py" ]; then
    echo "❌ Файл bot.py не найден. Запустите скрипт из корневой директории проекта."
    exit 1
fi

# Инициализируем git если нужно
if [ ! -d ".git" ]; then
    echo "📁 Инициализация git репозитория..."
    git init
    echo "✅ Git репозиторий инициализирован"
else
    echo "ℹ️  Git репозиторий уже существует"
fi

# Настраиваем git если нужно
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️  Настройка git..."
    git config --global user.name "Spelling Bot"
    git config --global user.email "bot@example.com"
    echo "✅ Git настроен"
fi

# Добавляем все файлы
echo "📝 Добавление файлов в git..."
git add .

# Создаем первый коммит
echo "💾 Создание первого коммита..."
git commit -m "Initial commit: Spelling bot with YandexGPT"

echo ""
echo "🎉 Git репозиторий готов!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Создайте репозиторий на GitHub"
echo "2. Добавьте remote:"
echo "   git remote add origin https://github.com/your-username/spelling-check-bot.git"
echo "3. Отправьте код:"
echo "   git push -u origin main"
echo ""
echo "🚀 После этого можно деплоить на сервер!" 