#!/bin/bash

ADMINS_FILE="/root/spelling-check-bot/admins.json"

echo "🔧 Управление администраторами бота"
echo "=================================="

# Функция для показа текущих администраторов
show_admins() {
    echo "📋 Текущие администраторы:"
    if [ -f "$ADMINS_FILE" ]; then
        cat "$ADMINS_FILE" | python3 -m json.tool
    else
        echo "❌ Файл admins.json не найден"
    fi
    echo
}

# Функция для добавления администратора
add_admin() {
    local user_id=$1
    if [ -z "$user_id" ]; then
        echo "❌ Укажите ID пользователя"
        return 1
    fi
    
    echo "➕ Добавляем администратора ID: $user_id"
    
    if [ -f "$ADMINS_FILE" ]; then
        # Добавляем к существующему списку
        python3 -c "
import json
try:
    with open('$ADMINS_FILE', 'r') as f:
        data = json.load(f)
    if $user_id not in data['admins']:
        data['admins'].append($user_id)
        with open('$ADMINS_FILE', 'w') as f:
            json.dump(data, f, indent=2)
        print('✅ Администратор добавлен')
    else:
        print('⚠️ Администратор уже существует')
except Exception as e:
    print(f'❌ Ошибка: {e}')
"
    else
        # Создаем новый файл
        echo "{\"admins\": [$user_id]}" > "$ADMINS_FILE"
        chmod 600 "$ADMINS_FILE"
        echo "✅ Файл создан и администратор добавлен"
    fi
}

# Функция для удаления администратора
remove_admin() {
    local user_id=$1
    if [ -z "$user_id" ]; then
        echo "❌ Укажите ID пользователя"
        return 1
    fi
    
    echo "➖ Удаляем администратора ID: $user_id"
    
    if [ -f "$ADMINS_FILE" ]; then
        python3 -c "
import json
try:
    with open('$ADMINS_FILE', 'r') as f:
        data = json.load(f)
    if $user_id in data['admins']:
        data['admins'].remove($user_id)
        with open('$ADMINS_FILE', 'w') as f:
            json.dump(data, f, indent=2)
        print('✅ Администратор удален')
    else:
        print('⚠️ Администратор не найден')
except Exception as e:
    print(f'❌ Ошибка: {e}')
"
    else
        echo "❌ Файл admins.json не найден"
    fi
}

# Функция для перезапуска бота
restart_bot() {
    echo "🔄 Перезапускаем бота..."
    sudo systemctl restart spelling-bot.service
    sudo systemctl status spelling-bot.service --no-pager
}

# Основное меню
case "$1" in
    "show"|"list")
        show_admins
        ;;
    "add")
        add_admin "$2"
        if [ $? -eq 0 ]; then
            restart_bot
        fi
        ;;
    "remove"|"delete")
        remove_admin "$2"
        if [ $? -eq 0 ]; then
            restart_bot
        fi
        ;;
    "restart")
        restart_bot
        ;;
    *)
        echo "Использование: $0 {show|add|remove|restart}"
        echo
        echo "Команды:"
        echo "  show     - показать текущих администраторов"
        echo "  add ID   - добавить администратора"
        echo "  remove ID - удалить администратора"
        echo "  restart  - перезапустить бота"
        echo
        echo "Примеры:"
        echo "  $0 show"
        echo "  $0 add 123456789"
        echo "  $0 remove 123456789"
        echo "  $0 restart"
        ;;
esac
