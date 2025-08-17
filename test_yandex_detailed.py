#!/usr/bin/env python3
"""
Детальная диагностика проблем с YandexGPT API
"""

import os
import requests
import json

# Устанавливаем переменные окружения
os.environ['YANDEX_API_KEY'] = 'AQVN18PYvPyNkfObkh7O9EWgcpXZzG47AEOc0lnU'
os.environ['YANDEX_FOLDER_ID'] = 'b1gvsm0staqq3jcivgl5'

def test_api_key_format():
    """Проверяет формат API ключа"""
    api_key = os.getenv('YANDEX_API_KEY')
    print(f"🔍 Проверка формата API ключа:")
    print(f"Длина ключа: {len(api_key)} символов")
    print(f"Начинается с: {api_key[:10]}...")
    print(f"Заканчивается на: ...{api_key[-10:]}")
    
    # Проверяем, что ключ начинается с AQVN (стандартный формат Yandex Cloud)
    if api_key.startswith('AQVN'):
        print("✅ Формат ключа корректный (начинается с AQVN)")
    else:
        print("❌ Необычный формат ключа")
    print()

def test_folder_id():
    """Проверяет формат Folder ID"""
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    print(f"🔍 Проверка Folder ID:")
    print(f"Folder ID: {folder_id}")
    print(f"Длина: {len(folder_id)} символов")
    
    # Проверяем формат (обычно начинается с b1g)
    if folder_id.startswith('b1g'):
        print("✅ Формат Folder ID корректный (начинается с b1g)")
    else:
        print("❌ Необычный формат Folder ID")
    print()

def test_different_auth_methods():
    """Тестирует разные способы аутентификации"""
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print("🔍 Тестирование разных способов аутентификации:")
    
    # Тест 1: Стандартный способ
    print("1️⃣ Тест стандартной аутентификации:")
    headers1 = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    test_request(headers1, "Стандартный Api-Key")
    
    # Тест 2: Bearer токен
    print("2️⃣ Тест Bearer токена:")
    headers2 = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    test_request(headers2, "Bearer токен")
    
    # Тест 3: Без префикса
    print("3️⃣ Тест без префикса:")
    headers3 = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    test_request(headers3, "Без префикса")

def test_request(headers, method_name):
    """Выполняет тестовый запрос"""
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    payload = {
        "modelUri": f"gpt://{os.getenv('YANDEX_FOLDER_ID')}/yandexgpt-lite",
        "completionOptions": {
            "temperature": 0.3,
            "maxTokens": 50
        },
        "messages": [
            {
                "role": "user",
                "text": "Привет"
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ {method_name} - РАБОТАЕТ!")
            result = response.json()
            if "result" in result and "alternatives" in result["result"]:
                text = result["result"]["alternatives"][0]["message"]["text"]
                print(f"   Ответ: {text}")
        elif response.status_code == 403:
            print(f"   ❌ {method_name} - Permission denied")
        elif response.status_code == 401:
            print(f"   ❌ {method_name} - Unauthorized")
        else:
            print(f"   ❌ {method_name} - Error {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ {method_name} - Exception: {e}")

def test_different_models():
    """Тестирует разные модели"""
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print("🔍 Тестирование разных моделей:")
    
    models = [
        "yandexgpt-lite",
        "yandexgpt",
        "yandexgpt-lite:latest",
        "yandexgpt:latest"
    ]
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    for model in models:
        print(f"🧪 Тестирую модель: {model}")
        
        payload = {
            "modelUri": f"gpt://{folder_id}/{model}",
            "completionOptions": {
                "temperature": 0.3,
                "maxTokens": 50
            },
            "messages": [
                {
                    "role": "user",
                    "text": "Привет"
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ {model} - РАБОТАЕТ!")
            elif response.status_code == 403:
                print(f"   ❌ {model} - Permission denied")
            elif response.status_code == 404:
                print(f"   ❌ {model} - Model not found")
            else:
                print(f"   ❌ {model} - Error {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {model} - Exception: {e}")
        
        print()

def main():
    """Основная функция диагностики"""
    print("🔍 Детальная диагностика YandexGPT API")
    print("=" * 60)
    
    test_api_key_format()
    test_folder_id()
    test_different_auth_methods()
    print()
    test_different_models()
    
    print("📋 Рекомендации:")
    print("1. Если все методы возвращают 403 - проблема в правах доступа")
    print("2. Если Bearer работает, а Api-Key нет - проблема в формате")
    print("3. Если некоторые модели работают - используйте работающую")
    print("4. Проверьте в Yandex Cloud Console:")
    print("   - Права сервисного аккаунта")
    print("   - Роль 'AI Language Model User'")
    print("   - Активность API ключа")

if __name__ == "__main__":
    main() 