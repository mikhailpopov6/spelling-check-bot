# 🚀 Руководство по развертыванию

## Локальное развертывание

### 1. Подготовка окружения
```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
```bash
# Создание файла .env
cp env_example.txt .env

# Редактирование файла .env
nano .env  # или любой текстовый редактор
```

### 3. Запуск
```bash
python bot.py
```

## Развертывание на сервере

### Ubuntu/Debian

#### 1. Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Git
sudo apt install git -y
```

#### 2. Клонирование и настройка
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd spelling-check-bot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp env_example.txt .env
nano .env
```

#### 3. Настройка systemd сервиса
```bash
# Создание файла сервиса
sudo nano /etc/systemd/system/spelling-bot.service
```

Содержимое файла сервиса:
```ini
[Unit]
Description=Spelling Check Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/spelling-check-bot
Environment=PATH=/path/to/spelling-check-bot/venv/bin
ExecStart=/path/to/spelling-check-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Запуск сервиса
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable spelling-bot

# Запуск сервиса
sudo systemctl start spelling-bot

# Проверка статуса
sudo systemctl status spelling-bot

# Просмотр логов
sudo journalctl -u spelling-bot -f
```

## Развертывание в Docker

### 1. Создание Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

### 2. Создание docker-compose.yml
```yaml
version: '3.8'

services:
  spelling-bot:
    build: .
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

### 3. Запуск с Docker
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## Развертывание на облачных платформах

### Heroku

#### 1. Подготовка
```bash
# Установка Heroku CLI
# Создание Procfile
echo "worker: python bot.py" > Procfile

# Создание runtime.txt
echo "python-3.11.0" > runtime.txt
```

#### 2. Развертывание
```bash
# Инициализация Git (если не сделано)
git init
git add .
git commit -m "Initial commit"

# Создание приложения на Heroku
heroku create your-bot-name

# Настройка переменных окружения
heroku config:set TELEGRAM_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key

# Развертывание
git push heroku main

# Запуск worker процесса
heroku ps:scale worker=1
```

### Railway

#### 1. Подготовка
- Подключите GitHub репозиторий к Railway
- Настройте переменные окружения в панели Railway

#### 2. Настройка
- Добавьте команду запуска: `python bot.py`
- Установите переменные окружения:
  - `TELEGRAM_TOKEN`
  - `OPENAI_API_KEY`

### Render

#### 1. Подготовка
- Подключите GitHub репозиторий к Render
- Создайте новый Web Service

#### 2. Настройка
- Build Command: `pip install -r requirements.txt`
- Start Command: `python bot.py`
- Environment Variables:
  - `TELEGRAM_TOKEN`
  - `OPENAI_API_KEY`

## Мониторинг и логирование

### Логирование
```bash
# Просмотр логов в реальном времени
tail -f bot.log

# Просмотр логов systemd
sudo journalctl -u spelling-bot -f

# Ротация логов
sudo logrotate /etc/logrotate.d/spelling-bot
```

### Мониторинг
```bash
# Проверка статуса бота
curl -X GET "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# Проверка использования ресурсов
htop
df -h
```

## Безопасность

### Рекомендации
1. Используйте HTTPS для всех соединений
2. Храните токены в переменных окружения
3. Регулярно обновляйте зависимости
4. Используйте firewall
5. Настройте rate limiting

### Обновление зависимостей
```bash
# Проверка уязвимостей
pip-audit

# Обновление зависимостей
pip install --upgrade -r requirements.txt
```

## Резервное копирование

### Настройка бэкапов
```bash
# Создание скрипта бэкапа
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/spelling-bot"
mkdir -p $BACKUP_DIR

# Бэкап кода
tar -czf $BACKUP_DIR/code_$DATE.tar.gz /path/to/spelling-check-bot

# Бэкап логов
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /path/to/logs

# Очистка старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
# Добавление в cron
chmod +x backup.sh
crontab -e
# Добавить строку: 0 2 * * * /path/to/backup.sh
``` 