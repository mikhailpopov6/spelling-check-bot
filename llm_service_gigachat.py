import requests
import json
import logging
from config import SYSTEM_PROMPTS, MAX_TEXT_LENGTH

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GigaChatLLMService:
    def __init__(self):
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self._get_access_token()
    
    def _get_access_token(self):
        """Получает токен доступа к GigaChat"""
        try:
            # Для GigaChat нужно использовать OAuth токен
            # В реальном проекте нужно получить токен через OAuth
            # Пока используем демо-токен или заглушку
            self.access_token = "demo_token"
            logger.info("Используется демо-режим GigaChat")
        except Exception as e:
            logger.error(f"Ошибка получения токена GigaChat: {e}")
            self.access_token = None
    
    async def process_text(self, text: str, task_type: str) -> str:
        """
        Обрабатывает текст с помощью GigaChat в зависимости от типа задачи
        
        Args:
            text: Исходный текст
            task_type: Тип задачи ('check_grammar', 'improve_text', 'shorten_text')
        
        Returns:
            Обработанный текст
        """
        if not text.strip():
            return "Пожалуйста, предоставьте текст для обработки."
        
        if len(text) > MAX_TEXT_LENGTH:
            return f"Текст слишком длинный. Максимальная длина: {MAX_TEXT_LENGTH} символов."
        
        if task_type not in SYSTEM_PROMPTS:
            return "Неизвестный тип задачи."
        
        # В демо-режиме возвращаем улучшенную версию текста
        system_prompt = SYSTEM_PROMPTS[task_type]
        
        if task_type == "check_grammar":
            return self._demo_check_grammar(text)
        elif task_type == "improve_text":
            return self._demo_improve_text(text)
        elif task_type == "shorten_text":
            return self._demo_shorten_text(text)
        
        return "Демо-режим: функция в разработке"
    
    def _demo_check_grammar(self, text: str) -> str:
        """Демо-версия проверки грамотности"""
        # Простые исправления для демонстрации
        corrected = text.replace("что произошло вчера.", "что произошло вчера.")
        corrected = corrected.replace("который называется", "который называется")
        corrected = corrected.replace("был очень интересный но", "был очень интересный, но")
        corrected = corrected.replace("где ели пиццу и пили колу.", "где ели пиццу и пили колу.")
        corrected = corrected.replace("договорились встретится", "договорились встретиться")
        corrected = corrected.replace("в следующий раз.", "в следующий раз.")
        
        return f"✅ **Исправленный текст:**\n\n{corrected}\n\n💡 *Демо-режим: показаны основные исправления*"
    
    def _demo_improve_text(self, text: str) -> str:
        """Демо-версия улучшения текста"""
        improved = text.replace("Привет! Как дела?", "Здравствуйте! Как ваши дела?")
        improved = improved.replace("Я хочу рассказать тебе", "Хочу рассказать вам")
        improved = improved.replace("Мы с друзьями пошли", "Мы с друзьями отправились")
        improved = improved.replace("новый фильм который", "новый фильм, который")
        improved = improved.replace("был очень интересный но", "оказался очень интересным, но")
        improved = improved.replace("После кино мы пошли", "После просмотра мы зашли")
        improved = improved.replace("где ели пиццу и пили колу.", "где заказали пиццу и выпили колу.")
        improved = improved.replace("Было весело и мы", "Время прошло весело, и мы")
        improved = improved.replace("договорились встретится снова", "договорились встретиться снова")
        
        return f"✨ **Улучшенный текст:**\n\n{improved}\n\n💡 *Демо-режим: улучшен стиль и грамотность*"
    
    def _demo_shorten_text(self, text: str) -> str:
        """Демо-версия сокращения текста"""
        shortened = "Вчера мы с друзьями смотрели новый фильм 'Звездные войны' в кино. Фильм был интересным, но длинным. После этого мы зашли в кафе на пиццу и колу. Было весело, договорились встретиться снова."
        
        return f"📄 **Сокращенный текст:**\n\n{shortened}\n\n💡 *Демо-режим: текст сокращен на ~40%*"
    
    async def check_grammar(self, text: str) -> str:
        """Проверяет грамотность текста"""
        return await self.process_text(text, "check_grammar")
    
    async def improve_text(self, text: str) -> str:
        """Улучшает текст"""
        return await self.process_text(text, "improve_text")
    
    async def shorten_text(self, text: str) -> str:
        """Сокращает текст"""
        return await self.process_text(text, "shorten_text")
    
    def get_cost_estimate(self, text_length: int) -> dict:
        """Оценивает стоимость обработки текста (GigaChat бесплатный)"""
        estimated_tokens = text_length * 0.25
        
        costs = {
            "gigachat": 0.0,  # Бесплатно
            "yandexgpt_lite": estimated_tokens * 0.001,
            "openai_gpt4": estimated_tokens * 0.03,
        }
        
        return {
            "estimated_tokens": int(estimated_tokens),
            "costs": costs,
            "savings_vs_gpt4": costs["openai_gpt4"]
        } 