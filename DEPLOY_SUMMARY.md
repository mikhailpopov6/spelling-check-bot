# 🚀 Краткая сводка по деплою

## 📁 Файлы для деплоя

### Основные файлы:
- `bot.py` - основной файл бота
- `llm_service.py` - сервис для работы с YandexGPT
- `config.py` - конфигурация
- `requirements.txt` - зависимости

### Файлы для деплоя:
- `deploy.sh` - полный скрипт деплоя с Supervisor
- `quick-deploy.sh` - быстрый деплой с Docker
- `init-git.sh` - инициализация git репозитория
- `Dockerfile` - контейнеризация
- `docker-compose.yml` - оркестрация контейнеров
- `DEPLOY_INSTRUCTIONS.md` - подробные инструкции

## 🚀 Быстрый старт

### 1. Подготовка локально:
```bash
# Инициализация git
./init-git.sh

# Создание репозитория на GitHub и отправка кода
git remote add origin https://github.com/your-username/spelling-check-bot.git
git push -u origin main
```

### 2. Деплой на сервер (Docker):
```bash
# Подключение к серверу
ssh root@your-server-ip

# Создание пользователя
adduser botuser
usermod -aG sudo botuser
su - botuser

# Клонирование и запуск
git clone https://github.com/your-username/spelling-check-bot.git
cd spelling-check-bot
./quick-deploy.sh
```

### 3. Настройка ключей:
```bash
# Редактирование .env файла
nano .env

# Добавление ключей:
TELEGRAM_TOKEN=your_telegram_token
YANDEX_API_KEY=your_yandex_api_key
YANDEX_FOLDER_ID=your_yandex_folder_id

# Перезапуск
docker-compose down
docker-compose up -d
```

## 🔄 Обновления

### Автоматическое обновление:
```bash
# На сервере
cd /opt/spelling-bot  # или где клонирован репозиторий
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Ручное обновление:
```bash
# Локально
git add .
git commit -m "Update"
git push origin main

# На сервере
./deploy.sh update
```

## 📊 Мониторинг

### Docker:
```bash
# Статус
docker-compose ps

# Логи
docker-compose logs -f

# Остановка
docker-compose down
```

### Supervisor:
```bash
# Статус
sudo supervisorctl status spelling-bot

# Логи
sudo tail -f /var/log/spelling-bot.out.log
```

## 💰 Стоимость

- **Digital Ocean**: $6/месяц (1GB RAM)
- **YandexGPT**: ~$0.001 за 1K токенов
- **Итого**: ~$6-10/месяц

## 🎯 Преимущества

### Docker версия:
- ✅ Простая установка
- ✅ Изоляция окружения
- ✅ Легкие обновления
- ✅ Портативность

### Supervisor версия:
- ✅ Прямая установка
- ✅ Меньше накладных расходов
- ✅ Полный контроль
- ✅ Автозапуск при перезагрузке

## 🛡️ Безопасность

1. Используйте SSH ключи
2. Настройте firewall
3. Не храните ключи в коде
4. Регулярно обновляйте систему

## 📞 Поддержка

При проблемах:
1. Проверьте логи
2. Убедитесь в правильности ключей
3. Проверьте права YandexGPT
4. Обратитесь к `DEPLOY_INSTRUCTIONS.md` 