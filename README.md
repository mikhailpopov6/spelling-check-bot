# 🤖 Spelling Check Bot

Многофункциональный Telegram бот для работы с русскими текстами. Поддерживает проверку грамотности, улучшение текста, сокращение и перевод на различные языки.

## ✨ Возможности

- **📝 Проверка грамотности** - исправляет орфографические и пунктуационные ошибки
- **✨ Улучшение текста** - делает текст более читаемым и грамотным
- **📄 Сокращение текста** - убирает лишние слова, сохраняя смысл
- **🌐 Перевод** - поддерживает перевод на английский, узбекский, армянский и с любого языка на русский
- **💡 Параметр nodot** - убирает точки в конце абзацев для любой команды
- **📊 Статистика** - отслеживает использование бота (для администраторов)

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/mikhailpopov6/spelling-check-bot.git
cd spelling-check-bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` на основе `env_example.txt`:
```bash
cp env_example.txt .env
```

Заполните `.env` файл:
```env
TELEGRAM_TOKEN=ваш_токен_бота
YANDEX_API_KEY=ваш_ключ_yandex
YANDEX_FOLDER_ID=ваш_folder_id
```

### 4. Запуск бота
```bash
python bot.py
```

## 📋 Команды бота

### Основные команды
- `/start` - Главное меню
- `/help` - Справка по использованию
- `/check [текст]` - Проверить грамотность
- `/improve [текст]` - Улучшить текст
- `/shorten [текст]` - Сократить текст
- `/translate [язык] [текст]` - Перевести текст

### Параметр nodot
К любой команде можно добавить `nodot` для удаления точек в конце абзацев:
- `/check [текст] nodot`
- `/improve [текст] nodot`
- `/shorten [текст] nodot`
- `/translate [язык] [текст] nodot`

### Поддерживаемые языки для перевода
- `en` - английский
- `uz` - узбекский
- `am` - армянский
- `ru` - русский (с автоопределением исходного языка)

### Примеры использования
```
/check Привет как дела
/check Привет как дела nodot
/improve Текст с ошибками
/translate en Привет мир
/translate ru Hello world
/translate uz Как дела
/translate ru Salom dunyo
```

## 🏗️ Структура проекта

```
spelling-check-bot/
├── bot.py              # Основная логика бота
├── config.py           # Конфигурация и промпты
├── llm_service.py      # Сервис для работы с YandexGPT
├── user_manager.py     # Управление пользователями и статистикой
├── requirements.txt    # Зависимости Python
├── env_example.txt     # Пример файла с переменными окружения
├── .gitignore         # Исключения для Git
├── README.md          # Документация
├── QUICKSTART.md      # Быстрый старт
└── CHANGELOG.md       # История изменений
```

## 🔧 Настройка

### Получение Telegram токена
1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### Получение Yandex Cloud API ключа
1. Зарегистрируйтесь в [Yandex Cloud](https://cloud.yandex.ru/)
2. Создайте платежный аккаунт
3. Создайте сервисный аккаунт
4. Получите API ключ для сервисного аккаунта
5. Скопируйте Folder ID из консоли

## 🚀 Развертывание на сервере

### Пошаговое развертывание

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и Git
sudo apt install python3 python3-pip python3-venv git -y
```

#### 2. Клонирование проекта
```bash
cd /root
git clone https://github.com/mikhailpopov6/spelling-check-bot.git
cd spelling-check-bot
```

#### 3. Настройка виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Настройка переменных окружения
```bash
cp env_example.txt .env
# Отредактируйте .env файл с вашими ключами
nano .env
```

#### 5. Создание systemd сервиса
```bash
sudo nano /etc/systemd/system/spelling-bot.service
```

Содержимое файла:
```ini
[Unit]
Description=Spelling Check Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/spelling-check-bot
Environment=PATH=/root/spelling-check-bot/venv/bin
ExecStart=/root/spelling-check-bot/venv/bin/python /root/spelling-check-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 6. Запуск сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable spelling-bot.service
sudo systemctl start spelling-bot.service
sudo systemctl status spelling-bot.service
```

#### 7. Просмотр логов
```bash
sudo journalctl -u spelling-bot.service -f
```

### Обновление бота
```bash
cd /root/spelling-check-bot
git pull
sudo systemctl restart spelling-bot.service
```

## 📊 Административные функции

### Команда статистики
- `/stats` - Показывает статистику использования бота (только для администраторов)

Для настройки администраторов отредактируйте `user_manager.py`:
```python
self.admins = [
    241666547,  # Ваш Telegram ID
]
```

## 🔒 Безопасность

- Все API ключи хранятся в файле `.env`
- Файл `.env` добавлен в `.gitignore`
- Пользовательские данные хранятся в `users.json`
- Файл `users.json` также добавлен в `.gitignore`

## 📝 Логирование

Бот ведет логи всех операций:
- Ошибки и исключения
- Запросы пользователей
- Статистика использования

## 🤝 Поддержка

Если у вас возникли вопросы или проблемы:
1. Проверьте логи: `sudo journalctl -u spelling-bot.service -f`
2. Убедитесь, что все переменные окружения настроены правильно
3. Проверьте статус сервиса: `sudo systemctl status spelling-bot.service`

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. 