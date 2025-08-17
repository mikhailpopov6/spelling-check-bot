#!/usr/bin/env python3
"""
Тест для проверки доступности каталога и других сервисов Yandex Cloud
"""

import os
import requests
import json

# Устанавливаем переменные окружения
os.environ['YANDEX_API_KEY'] = 'AQVN18PYvPyNkfObkh7O9EWgcpXZzG47AEOc0lnU'
os.environ['YANDEX_FOLDER_ID'] = 'b1gvsm0staqq3jcivgl5'

def test_catalog_access():
    """Тестирует доступность каталога"""
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print("🔍 Тестирование доступа к каталогу:")
    
    # Тест 1: Получение информации о каталоге
    url = f"https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/{folder_id}"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Каталог доступен!")
            print(f"   Название: {result.get('name', 'Не указано')}")
            print(f"   Описание: {result.get('description', 'Не указано')}")
            print(f"   Статус: {result.get('status', 'Не указано')}")
        elif response.status_code == 403:
            print(f"❌ Нет доступа к каталогу (403)")
        elif response.status_code == 404:
            print(f"❌ Каталог не найден (404)")
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к каталогу: {e}")
    
    print()

def test_service_accounts():
    """Тестирует доступ к сервисным аккаунтам"""
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print("🔍 Тестирование доступа к сервисным аккаунтам:")
    
    url = f"https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "folderId": folder_id
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            accounts = result.get('serviceAccounts', [])
            print(f"✅ Найдено сервисных аккаунтов: {len(accounts)}")
            
            for account in accounts:
                print(f"   - {account.get('name', 'Без имени')} (ID: {account.get('id', 'Нет ID')})")
                
        elif response.status_code == 403:
            print(f"❌ Нет доступа к сервисным аккаунтам (403)")
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к сервисным аккаунтам: {e}")
    
    print()

def test_iam_roles():
    """Тестирует доступ к ролям IAM"""
    api_key = os.getenv('YANDEX_API_KEY')
    
    print("🔍 Тестирование доступа к ролям IAM:")
    
    url = "https://iam.api.cloud.yandex.net/iam/v1/roles"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            roles = result.get('roles', [])
            print(f"✅ Найдено ролей: {len(roles)}")
            
            # Ищем роль для YandexGPT
            ai_roles = [role for role in roles if 'ai' in role.get('id', '').lower() or 'language' in role.get('id', '').lower()]
            
            if ai_roles:
                print("   Роли, связанные с AI:")
                for role in ai_roles:
                    print(f"   - {role.get('id', 'Нет ID')}: {role.get('title', 'Без названия')}")
            else:
                print("   Роли для AI не найдены")
                
        elif response.status_code == 403:
            print(f"❌ Нет доступа к ролям IAM (403)")
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к ролям IAM: {e}")
    
    print()

def test_operation_log():
    """Тестирует доступ к логам операций"""
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print("🔍 Тестирование доступа к логам операций:")
    
    url = f"https://operation.api.cloud.yandex.net/operations"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    params = {
        "folderId": folder_id,
        "pageSize": 5
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            operations = result.get('operations', [])
            print(f"✅ Найдено операций: {len(operations)}")
            
            for op in operations:
                print(f"   - {op.get('description', 'Без описания')} (статус: {op.get('done', False)})")
                
        elif response.status_code == 403:
            print(f"❌ Нет доступа к логам операций (403)")
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при обращении к логам операций: {e}")
    
    print()

def main():
    """Основная функция тестирования"""
    print("🔍 Тестирование доступа к сервисам Yandex Cloud")
    print("=" * 60)
    
    test_catalog_access()
    test_service_accounts()
    test_iam_roles()
    test_operation_log()
    
    print("📋 Анализ результатов:")
    print("1. Если каталог недоступен - проблема с правами на каталог")
    print("2. Если сервисные аккаунты недоступны - проблема с правами IAM")
    print("3. Если роли недоступны - проблема с правами администратора")
    print("4. Если все доступно, но YandexGPT не работает - проблема с конкретной ролью")

if __name__ == "__main__":
    main() 