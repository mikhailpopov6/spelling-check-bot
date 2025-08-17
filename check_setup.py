#!/usr/bin/env python3
"""
Скрипт для проверки правильности установки и настройки бота с YandexGPT
"""

import os
import sys
from dotenv import load_dotenv

def check_python_version():
    """Проверяет версию Python"""
    print("🐍 Проверка версии Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Требуется Python 3.8+, установлена {version.major}.{version.minor}.{version.micro}")
        return False

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("\n📦 Проверка зависимостей...")
    
    required_packages = [
        'telegram',
        'yandexcloud',
        'python-dotenv',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - установлен")
        except ImportError:
            print(f"❌ {package} - НЕ установлен")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите их командой: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Проверяет наличие и содержимое файла .env"""
    print("\n🔧 Проверка файла .env...")
    
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        print("Создайте файл .env на основе env_example.txt")
        return False
    
    load_dotenv()
    
    required_vars = ['TELEGRAM_TOKEN', 'YANDEX_API_KEY', 'YANDEX_FOLDER_ID']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f'your_{var.lower()}_here':
            print(f"✅ {var} - настроен")
        else:
            print(f"❌ {var} - НЕ настроен")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Не настроены переменные: {', '.join(missing_vars)}")
        print("Отредактируйте файл .env и добавьте правильные значения")
        print("\n📋 Как получить ключи Yandex Cloud:")
        print("1. Зарегистрируйтесь на https://cloud.yandex.ru/")
        print("2. Создайте платежный аккаунт")
        print("3. Создайте каталог (folder)")
        print("4. Получите API ключ в разделе 'Сервисные аккаунты'")
        print("5. Скопируйте ID каталога")
        return False
    
    return True

def check_files():
    """Проверяет наличие всех необходимых файлов"""
    print("\n📁 Проверка файлов проекта...")
    
    required_files = [
        'bot.py',
        'llm_service.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - найден")
        else:
            print(f"❌ {file} - НЕ найден")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    return True

def show_cost_comparison():
    """Показывает сравнение стоимости разных LLM"""
    print("\n💰 Сравнение стоимости LLM (за 1K токенов):")
    print("   OpenAI GPT-4:     $0.030")
    print("   OpenAI GPT-3.5:   $0.002")
    print("   YandexGPT:        $0.002")
    print("   YandexGPT Lite:   $0.001")
    print("   GigaChat:         Бесплатно")
    print("\n💡 YandexGPT в 15-30 раз дешевле GPT-4!")

def main():
    """Основная функция проверки"""
    print("🔍 Проверка установки бота для работы с русскими текстами")
    print("🤖 Используется: YandexGPT (оптимизирован для русского языка)")
    print("=" * 70)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_files()
    ]
    
    show_cost_comparison()
    
    print("\n" + "=" * 70)
    
    if all(checks):
        print("🎉 Все проверки пройдены успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Запустите тест: python test_llm.py")
        print("2. Запустите бота: python bot.py")
        print("3. Найдите бота в Telegram и отправьте /start")
        print("\n💡 Преимущества YandexGPT:")
        print("   ✅ Лучше работает с русским языком")
        print("   ✅ В 15-30 раз дешевле OpenAI")
        print("   ✅ Быстрая обработка")
        print("   ✅ Надежная инфраструктура")
    else:
        print("❌ Обнаружены проблемы с установкой")
        print("\n📋 Рекомендации:")
        print("1. Установите недостающие зависимости: pip install -r requirements.txt")
        print("2. Настройте файл .env с правильными ключами Yandex Cloud")
        print("3. Убедитесь, что все файлы проекта на месте")
        print("4. Обратитесь к документации в README.md")

if __name__ == "__main__":
    main() 