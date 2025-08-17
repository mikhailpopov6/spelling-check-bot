# 🚀 Инструкции по деплою на Digital Ocean

## 📋 Подготовка

### 1. Создание репозитория на GitHub
```bash
# Инициализируем git (если еще не сделано)
git init
git add .
git commit -m "Initial commit"

# Создайте репозиторий на GitHub и добавьте remote
git remote add origin https://github.com/your-username/spelling-check-bot.git
git push -u origin main
```

### 2. Создание Droplet на Digital Ocean
1. Зайдите в [Digital Ocean Console](https://cloud.digitalocean.com/)
2. Нажмите "Create" → "Droplets"
3. Выберите:
   - **Ubuntu 22.04 LTS**
   - **Basic Plan**
   - **Regular CPU** (1GB RAM, 1 vCPU)
   - **Datacenter** ближайший к вам
4. Добавьте SSH ключ (рекомендуется)
5. Нажмите "Create Droplet"

## 🚀 Вариант 1: Быстрый деплой с Docker (Рекомендуется)

### Шаг 1: Подключение к серверу
```bash
ssh root@your-server-ip
```

### Шаг 2: Создание пользователя
```bash
# Создаем пользователя
adduser botuser
usermod -aG sudo botuser

# Переключаемся на пользователя
su - botuser
```

### Шаг 3: Клонирование и запуск
```bash
# Клонируем репозиторий
git clone https://github.com/your-username/spelling-check-bot.git
cd spelling-check-bot

# Делаем скрипт исполняемым
chmod +x quick-deploy.sh

# Запускаем быстрый деплой
./quick-deploy.sh
```

### Шаг 4: Настройка переменных окружения
```bash
# Редактируем .env файл
nano .env

# Добавляем ваши ключи:
TELEGRAM_TOKEN=your_telegram_token
YANDEX_API_KEY=your_yandex_api_key
YANDEX_FOLDER_ID=your_yandex_folder_id
```

### Шаг 5: Перезапуск с новыми ключами
```bash
docker-compose down
docker-compose up -d
```

## 🚀 Вариант 2: Классический деплой с Supervisor

### Шаг 1: Подключение к серверу
```bash
ssh root@your-server-ip
```

### Шаг 2: Запуск установки
```bash
# Клонируем репозиторий
git clone https://github.com/your-username/spelling-check-bot.git
cd spelling-check-bot

# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем установку
./deploy.sh install
```

### Шаг 3: Настройка переменных окружения
```bash
# Редактируем .env файл
nano /opt/spelling-bot/.env

# Добавляем ваши ключи
```

### Шаг 4: Перезапуск бота
```bash
sudo supervisorctl restart spelling-bot
```

## 🔄 Обновления

### Для Docker версии:
```bash
# Обновление кода
git pull origin main

# Пересборка и перезапуск
docker-compose down
docker-compose up -d --build
```

### Для Supervisor версии:
```bash
# Обновление
./deploy.sh update
```

## 📊 Мониторинг

### Docker версия:
```bash
# Статус
docker-compose ps

# Логи
docker-compose logs -f

# Остановка
docker-compose down
```

### Supervisor версия:
```bash
# Статус
sudo supervisorctl status spelling-bot

# Логи
sudo tail -f /var/log/spelling-bot.out.log

# Остановка
sudo supervisorctl stop spelling-bot
```

## 🔧 Устранение неполадок

### Проблема: Бот не отвечает
```bash
# Проверяем логи
docker-compose logs spelling-bot
# или
sudo tail -f /var/log/spelling-bot.out.log

# Проверяем переменные окружения
cat .env
```

### Проблема: Ошибки YandexGPT
```bash
# Проверяем права доступа
python3 test_yandex_debug.py
```

### Проблема: Порт занят
```bash
# Проверяем процессы
ps aux | grep python
# или
docker ps
```

## 💰 Стоимость

- **Digital Ocean Droplet**: $6/месяц (1GB RAM, 1 vCPU)
- **YandexGPT**: ~$0.001 за 1K токенов
- **Telegram Bot**: Бесплатно

**Общая стоимость**: ~$6-10/месяц

## 🛡️ Безопасность

### Рекомендации:
1. Используйте SSH ключи вместо паролей
2. Настройте firewall (UFW)
3. Регулярно обновляйте систему
4. Не храните ключи в коде
5. Используйте HTTPS для всех соединений

### Настройка firewall:
```bash
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## 📈 Масштабирование

### Для увеличения нагрузки:
1. Увеличьте RAM до 2GB ($12/месяц)
2. Добавьте мониторинг (Prometheus + Grafana)
3. Настройте автоматические бэкапы
4. Добавьте load balancer при необходимости

## 🎯 Автоматизация

### GitHub Actions для автоматического деплоя:
Создайте `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Digital Ocean

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.4
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.KEY }}
        script: |
          cd /opt/spelling-bot
          git pull origin main
          docker-compose down
          docker-compose up -d --build
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи
2. Убедитесь, что все ключи правильные
3. Проверьте права доступа к YandexGPT
4. Обратитесь к документации Yandex Cloud 