# 🚀 Быстрый старт - Spelling Check Bot

Пошаговое руководство по запуску бота за 5 минут.

## 📋 Предварительные требования

- Python 3.8+
- Telegram аккаунт
- Yandex Cloud аккаунт (бесплатный)

## ⚡ Быстрая установка

### Шаг 1: Клонирование
```bash
git clone https://github.com/mikhailpopov6/spelling-check-bot.git
cd spelling-check-bot
```

### Шаг 2: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 3: Настройка ключей
```bash
cp env_example.txt .env
```

Отредактируйте `.env` файл:
```env
TELEGRAM_TOKEN=ваш_токен_бота
YANDEX_API_KEY=ваш_ключ_yandex
YANDEX_FOLDER_ID=ваш_folder_id
```

### Шаг 4: Запуск
```bash
python bot.py
```

## 🔑 Получение ключей

### Telegram Bot Token
1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

### Yandex Cloud API
1. Зарегистрируйтесь на [cloud.yandex.ru](https://cloud.yandex.ru/)
2. Создайте платежный аккаунт (бесплатно)
3. Создайте сервисный аккаунт
4. Получите API ключ
5. Скопируйте Folder ID

## 📱 Использование

### Основные команды
- `/start` - Главное меню
- `/check [текст]` - Проверить грамотность
- `/improve [текст]` - Улучшить текст
- `/shorten [текст]` - Сократить текст
- `/translate [язык] [текст]` - Перевести

### Примеры
```
/check Привет как дела
/improve Текст с ошибками
/translate en Привет мир
/translate ru Hello world
```

### Параметр nodot
Добавьте `nodot` к любой команде для удаления точек в конце абзацев:
```
/check Привет как дела nodot
/translate en Привет мир nodot
```

## 🌐 Поддерживаемые языки перевода
- `en` - английский
- `uz` - узбекский
- `am` - армянский
- `ru` - русский (с автоопределением)

## 🚀 Развертывание на сервере

### Ubuntu/Debian
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
sudo apt install python3 python3-pip python3-venv git -y

# Клонирование
cd /root
git clone https://github.com/mikhailpopov6/spelling-check-bot.git
cd spelling-check-bot

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка
cp env_example.txt .env
nano .env  # Отредактируйте ключи

# Создание сервиса
sudo nano /etc/systemd/system/spelling-bot.service
```

Содержимое сервиса:
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

```bash
# Запуск
sudo systemctl daemon-reload
sudo systemctl enable spelling-bot.service
sudo systemctl start spelling-bot.service

# Проверка
sudo systemctl status spelling-bot.service
```

## 🔧 Управление

### Просмотр логов
```bash
sudo journalctl -u spelling-bot.service -f
```

### Обновление
```bash
cd /root/spelling-check-bot
git pull
sudo systemctl restart spelling-bot.service
```

### Остановка
```bash
sudo systemctl stop spelling-bot.service
```

## 📊 Административные функции

### Статистика
- `/stats` - Показывает статистику (только для админов)

### Настройка администраторов
Отредактируйте `user_manager.py`:
```python
self.admins = [
    241666547,  # Ваш Telegram ID
]
```

## 🆘 Решение проблем

### Бот не отвечает
1. Проверьте статус: `sudo systemctl status spelling-bot.service`
2. Посмотрите логи: `sudo journalctl -u spelling-bot.service -f`
3. Проверьте ключи в `.env`

### Ошибки API
1. Убедитесь, что Yandex Cloud API ключ правильный
2. Проверьте Folder ID
3. Убедитесь, что есть средства на балансе

### Проблемы с Telegram
1. Проверьте правильность токена
2. Убедитесь, что бот не заблокирован
3. Проверьте права бота

## 📞 Поддержка

Если что-то не работает:
1. Проверьте логи
2. Убедитесь в правильности ключей
3. Проверьте статус сервиса
4. Перезапустите бота

## 🎯 Что дальше?

После успешного запуска:
1. Протестируйте все команды
2. Настройте администраторов
3. Добавьте бота в нужные чаты
4. Настройте мониторинг логов 