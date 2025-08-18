import requests
import json
import logging
import re
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID, YANDEX_MODEL, SYSTEM_PROMPTS, MAX_TEXT_LENGTH

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        if not YANDEX_API_KEY:
            raise ValueError("YANDEX_API_KEY не найден в переменных окружения")
        if not YANDEX_FOLDER_ID:
            raise ValueError("YANDEX_FOLDER_ID не найден в переменных окружения")
        
        self.api_key = YANDEX_API_KEY
        self.folder_id = YANDEX_FOLDER_ID
        self.model = YANDEX_MODEL
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    def fix_dashes(self, text: str) -> str:
        """
        Заменяет длинные тире (—) на средние тире (–)
        
        Args:
            text: Исходный текст
        
        Returns:
            Текст с исправленными тире
        """
        # Заменяем длинные тире (em dash) на средние тире (en dash)
        text = re.sub(r'—', '–', text)
        # Также заменяем обычные тире на средние тире для единообразия
        text = re.sub(r'(?<![\w])-(?![\w])', '–', text)
        return text
    
    async def process_text(self, text: str, task_type: str) -> str:
        """
        Обрабатывает текст с помощью YandexGPT в зависимости от типа задачи
        
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
        
        try:
            system_prompt = SYSTEM_PROMPTS[task_type]
            
            # Формируем запрос к YandexGPT
            headers = {
                "Authorization": f"Api-Key {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "modelUri": f"gpt://{self.folder_id}/{self.model}",
                "completionOptions": {
                    "temperature": 0.3,
                    "maxTokens": 2000
                },
                "messages": [
                    {
                        "role": "system",
                        "text": system_prompt
                    },
                    {
                        "role": "user",
                        "text": f"Обработай следующий текст:\n\n{text}"
                    }
                ]
            }
            
            # Отправляем запрос
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "result" in result and "alternatives" in result["result"]:
                    text_result = result["result"]["alternatives"][0]["message"]["text"].strip()
                    # Исправляем тире в результате
                    text_result = self.fix_dashes(text_result)
                    logger.info(f"Успешно обработан текст для задачи: {task_type}")
                    return text_result
                else:
                    logger.error(f"Неожиданная структура ответа: {result}")
                    return "Ошибка при обработке ответа от модели."
            else:
                logger.error(f"Ошибка API: {response.status_code} - {response.text}")
                return f"Ошибка API: {response.status_code}"
            
        except requests.exceptions.Timeout:
            logger.error("Таймаут при запросе к YandexGPT")
            return "Превышено время ожидания ответа. Попробуйте позже."
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при запросе к YandexGPT: {e}")
            return f"Ошибка сети: {str(e)}"
        except Exception as e:
            logger.error(f"Ошибка при обработке текста: {e}")
            return f"Произошла ошибка при обработке текста: {str(e)}"
    
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
        """
        Оценивает стоимость обработки текста
        
        Args:
            text_length: Длина текста в символах
        
        Returns:
            Словарь с оценкой стоимости
        """
        # Примерная оценка: 1 символ ≈ 0.25 токена
        estimated_tokens = text_length * 0.25
        
        costs = {
            "yandexgpt_lite": estimated_tokens * 0.001,
            "yandexgpt": estimated_tokens * 0.002,
            "openai_gpt4": estimated_tokens * 0.03,
            "openai_gpt35": estimated_tokens * 0.002
        }
        
        return {
            "estimated_tokens": int(estimated_tokens),
            "costs": costs,
            "savings_vs_gpt4": costs["openai_gpt4"] - costs["yandexgpt_lite"]
        } 