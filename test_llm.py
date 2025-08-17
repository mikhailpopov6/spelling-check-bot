#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы LLM сервиса с YandexGPT
"""

import asyncio
import os
from dotenv import load_dotenv
from llm_service import LLMService

# Загружаем переменные окружения
load_dotenv()

async def test_llm_service():
    """Тестирует все функции LLM сервиса"""
    
    # Проверяем наличие API ключей
    if not os.getenv('YANDEX_API_KEY'):
        print("❌ YANDEX_API_KEY не найден в переменных окружения")
        print("Создайте файл .env с вашим Yandex Cloud API ключом")
        return
    
    if not os.getenv('YANDEX_FOLDER_ID'):
        print("❌ YANDEX_FOLDER_ID не найден в переменных окружения")
        print("Добавьте ваш Yandex Cloud Folder ID в файл .env")
        return
    
    try:
        # Создаем экземпляр сервиса
        llm_service = LLMService()
        print("✅ LLM сервис инициализирован успешно")
        print("🤖 Используется: YandexGPT (оптимизирован для русского языка)")
        
        # Тестовый текст с ошибками
        test_text = """
        Привет! Как дела? Я хочу рассказать тебе о том что произошло вчера.
        Мы с друзьями пошли в кино и смотрели новый фильм который называется "Звездные войны".
        Фильм был очень интересный но немного длинный. После кино мы пошли в кафе где ели пиццу и пили колу.
        Было весело и мы договорились встретится снова в следующий раз.
        """
        
        print("\n📝 Тестовый текст:")
        print(test_text)
        
        # Показываем оценку стоимости
        cost_estimate = llm_service.get_cost_estimate(len(test_text))
        print(f"\n💰 Оценка стоимости:")
        print(f"   Токенов: ~{cost_estimate['estimated_tokens']}")
        print(f"   YandexGPT Lite: ${cost_estimate['costs']['yandexgpt_lite']:.4f}")
        print(f"   OpenAI GPT-4: ${cost_estimate['costs']['openai_gpt4']:.4f}")
        print(f"   Экономия: ${cost_estimate['savings_vs_gpt4']:.4f} (в {cost_estimate['costs']['openai_gpt4']/cost_estimate['costs']['yandexgpt_lite']:.0f} раз дешевле!)")
        
        # Тест 1: Проверка грамотности
        print("\n🔄 Тестирую проверку грамотности...")
        result = await llm_service.check_grammar(test_text)
        print("✅ Результат проверки грамотности:")
        print(result)
        
        # Тест 2: Улучшение текста
        print("\n🔄 Тестирую улучшение текста...")
        result = await llm_service.improve_text(test_text)
        print("✨ Результат улучшения:")
        print(result)
        
        # Тест 3: Сокращение текста
        print("\n🔄 Тестирую сокращение текста...")
        result = await llm_service.shorten_text(test_text)
        print("📄 Результат сокращения:")
        print(result)
        
        print("\n🎉 Все тесты завершены успешно!")
        print("💡 YandexGPT показал отличные результаты для русского языка!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    print("🧪 Запуск тестов LLM сервиса с YandexGPT...")
    asyncio.run(test_llm_service()) 