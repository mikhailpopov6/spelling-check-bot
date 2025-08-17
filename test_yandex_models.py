#!/usr/bin/env python3
"""
Скрипт для тестирования разных моделей YandexGPT
"""

import os
import requests
import json

# Устанавливаем переменные окружения
os.environ['YANDEX_API_KEY'] = 'AQVN18PYvPyNkfObkh7O9EWgcpXZzG47AEOc0lnU'
os.environ['YANDEX_FOLDER_ID'] = 'b1gvsm0staqq3jcivgl5'

def test_model(model_name):
    """Тестирует конкретную модель"""
    
    api_key = os.getenv('YANDEX_API_KEY')
    folder_id = os.getenv('YANDEX_FOLDER_ID')
    
    print(f"🧪 Тестирую модель: {model_name}")
    
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    headers = {
        "Authorization": f"Api-Key {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "modelUri": f"gpt://{folder_id}/{model_name}",
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
            print(f"✅ {model_name} - РАБОТАЕТ!")
            result = response.json()
            if "result" in result and "alternatives" in result["result"]:
                text = result["result"]["alternatives"][0]["message"]["text"]
                print(f"   Ответ: {text}")
        elif response.status_code == 403:
            print(f"❌ {model_name} - Permission denied")
        elif response.status_code == 404:
            print(f"❌ {model_name} - Model not found")
        else:
            print(f"❌ {model_name} - Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ {model_name} - Exception: {e}")
    
    print()

def main():
    """Тестирует все доступные модели"""
    
    print("🔍 Тестирование моделей YandexGPT")
    print("=" * 50)
    
    # Список моделей для тестирования
    models = [
        "yandexgpt-lite",
        "yandexgpt",
        "yandexgpt-lite:latest",
        "yandexgpt:latest",
        "gpt://b1gvsm0staqq3jcivgl5/yandexgpt-lite",
        "gpt://b1gvsm0staqq3jcivgl5/yandexgpt"
    ]
    
    for model in models:
        test_model(model)
    
    print("📋 Рекомендации:")
    print("1. Если все модели возвращают 403 - проблема в правах доступа")
    print("2. Если некоторые модели работают - используйте работающую")
    print("3. Если все модели возвращают 404 - проверьте Folder ID")

if __name__ == "__main__":
    main() 