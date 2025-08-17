#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с YandexGPT API
"""

import os
import requests
import json

# Устанавливаем переменные окружения
os.environ['TELEGRAM_TOKEN'] = '8475569974:AAF1MWVwTail48jAWkpkQfx4hLk6aX9c3aI'
os.environ['YANDEX_API_KEY'] = 'AQVN18PYvPyNkfObkh7O9EWgcpXZzG47AEOc0lnU'
os.environ['YANDEX_FOLDER_ID'] = 'b1gvsm0staqq3jcivgl5'

def test_yandex_api():
    """Тестирует подключение к YandexGPT API"""
    
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print(f"🔍 Диагностика YandexGPT API")
    print(f"API Key: {api_key[:10]}..." if api_key else "❌ API Key не найден")
    print(f"Folder ID: {folder_id}")
    print()
    
    if not api_key or not folder_id:
        print("❌ Отсутствуют необходимые ключи")
        return
    
    # Тестовый запрос
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
        "completionOptions": {
            "temperature": 0.3,
            "maxTokens": 100
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты помощник для работы с русским языком."
            },
            {
                "role": "user",
                "text": "Привет! Как дела?"
            }
        ]
    }
    
    print("📡 Отправляем тестовый запрос...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Ответ сервера:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Запрос успешен!")
            if "result" in result and "alternatives" in result["result"]:
                text = result["result"]["alternatives"][0]["message"]["text"]
                print(f"Ответ модели: {text}")
        elif response.status_code == 403:
            print("❌ Ошибка 403: Permission denied")
            print("Возможные причины:")
            print("1. Неправильный API ключ")
            print("2. У сервисного аккаунта нет прав на YandexGPT")
            print("3. Неправильный Folder ID")
            print("4. Сервисный аккаунт не активирован")
        elif response.status_code == 401:
            print("❌ Ошибка 401: Unauthorized")
            print("Возможные причины:")
            print("1. Неправильный API ключ")
            print("2. API ключ истек")
        else:
            print(f"❌ Неожиданная ошибка: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Таймаут при запросе")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка сети: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

def check_yandex_cloud_setup():
    """Проверяет настройки Yandex Cloud"""
    print("🔧 Проверка настроек Yandex Cloud:")
    print()
    print("1. Убедитесь, что вы зарегистрированы на https://cloud.yandex.ru/")
    print("2. Проверьте, что у вас есть платежный аккаунт")
    print("3. Убедитесь, что каталог (folder) существует")
    print("4. Проверьте права сервисного аккаунта:")
    print("   - Перейдите в 'Сервисные аккаунты'")
    print("   - Найдите ваш аккаунт")
    print("   - Убедитесь, что назначена роль 'AI Language Model User'")
    print("5. Проверьте, что API ключ активен")
    print()

if __name__ == "__main__":
    test_yandex_api()
    print()
    check_yandex_cloud_setup() 