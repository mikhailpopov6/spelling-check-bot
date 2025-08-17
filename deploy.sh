#!/bin/bash

# Скрипт для деплоя бота на Digital Ocean
# Использование: ./deploy.sh [update|install]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для вывода
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверяем, что мы в правильной директории
if [ ! -f "bot.py" ]; then
    log_error "Файл bot.py не найден. Запустите скрипт из корневой директории проекта."
    exit 1
fi

# Функция для установки на сервере
install_on_server() {
    log_info "Установка бота на сервере..."
    
    # Обновляем систему
    log_info "Обновление системы..."
    sudo apt update && sudo apt upgrade -y
    
    # Устанавливаем Python и pip
    log_info "Установка Python и зависимостей..."
    sudo apt install python3 python3-pip python3-venv git supervisor -y
    
    # Создаем директорию для бота
    log_info "Создание директории для бота..."
    sudo mkdir -p /opt/spelling-bot
    sudo chown $USER:$USER /opt/spelling-bot
    
    # Клонируем репозиторий
    log_info "Клонирование репозитория..."
    cd /opt/spelling-bot
    if [ -d ".git" ]; then
        log_warning "Репозиторий уже существует. Обновляем..."
        git pull origin main
    else
        git clone https://github.com/your-username/spelling-check-bot.git .
    fi
    
    # Создаем виртуальное окружение
    log_info "Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Устанавливаем зависимости
    log_info "Установка зависимостей..."
    pip install -r requirements.txt
    
    # Создаем файл .env
    log_info "Создание файла .env..."
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Telegram Bot Token
TELEGRAM_TOKEN=your_telegram_token_here

# Yandex Cloud API
YANDEX_API_KEY=your_yandex_api_key_here
YANDEX_FOLDER_ID=your_yandex_folder_id_here
EOF
        log_warning "Файл .env создан. Отредактируйте его с вашими ключами!"
    fi
    
    # Создаем конфигурацию supervisor
    log_info "Настройка supervisor..."
    sudo tee /etc/supervisor/conf.d/spelling-bot.conf > /dev/null << EOF
[program:spelling-bot]
command=/opt/spelling-bot/venv/bin/python bot.py
directory=/opt/spelling-bot
user=$USER
autostart=true
autorestart=true
stderr_logfile=/var/log/spelling-bot.err.log
stdout_logfile=/var/log/spelling-bot.out.log
environment=PYTHONUNBUFFERED=1
EOF
    
    # Перезапускаем supervisor
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start spelling-bot
    
    log_success "Установка завершена!"
    log_info "Проверьте статус: sudo supervisorctl status spelling-bot"
    log_info "Просмотр логов: sudo tail -f /var/log/spelling-bot.out.log"
}

# Функция для обновления на сервере
update_on_server() {
    log_info "Обновление бота на сервере..."
    
    cd /opt/spelling-bot
    
    # Останавливаем бота
    log_info "Остановка бота..."
    sudo supervisorctl stop spelling-bot
    
    # Обновляем код
    log_info "Обновление кода..."
    git pull origin main
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    
    # Обновляем зависимости
    log_info "Обновление зависимостей..."
    pip install -r requirements.txt
    
    # Запускаем бота
    log_info "Запуск бота..."
    sudo supervisorctl start spelling-bot
    
    log_success "Обновление завершено!"
    log_info "Проверьте статус: sudo supervisorctl status spelling-bot"
}

# Функция для локального деплоя
deploy_from_local() {
    log_info "Подготовка к деплою..."
    
    # Проверяем, что все файлы на месте
    required_files=("bot.py" "llm_service.py" "config.py" "requirements.txt")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Файл $file не найден!"
            exit 1
        fi
    done
    
    # Создаем .gitignore если его нет
    if [ ! -f ".gitignore" ]; then
        log_warning "Создание .gitignore..."
        cat > .gitignore << EOF
# Переменные окружения
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Temporary files
*.tmp
*.temp
EOF
    fi
    
    # Инициализируем git если нужно
    if [ ! -d ".git" ]; then
        log_info "Инициализация git репозитория..."
        git init
        git add .
        git commit -m "Initial commit"
        log_warning "Создайте репозиторий на GitHub и добавьте remote:"
        log_warning "git remote add origin https://github.com/your-username/spelling-check-bot.git"
        log_warning "git push -u origin main"
    else
        log_info "Обновление git репозитория..."
        git add .
        git commit -m "Update bot $(date)"
        git push origin main
    fi
    
    log_success "Локальная подготовка завершена!"
}

# Основная логика
case "${1:-deploy}" in
    "install")
        install_on_server
        ;;
    "update")
        update_on_server
        ;;
    "deploy")
        deploy_from_local
        ;;
    *)
        log_error "Неизвестная команда: $1"
        log_info "Использование: $0 [deploy|install|update]"
        log_info "  deploy  - подготовка к деплою (локально)"
        log_info "  install - установка на сервере"
        log_info "  update  - обновление на сервере"
        exit 1
        ;;
esac 