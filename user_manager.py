import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, data_file: str = "users.json"):
        self.data_file = data_file
        self.users = self.load_users()
        
        # Админы (Telegram ID)
        self.admins = [
            123456789,  # Замените на ваш Telegram ID
            # Добавьте других админов здесь
        ]
    
    def load_users(self) -> Dict:
        """Загружает данные пользователей из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Ошибка загрузки данных пользователей: {e}")
                return {}
        return {}
    
    def save_users(self):
        """Сохраняет данные пользователей в файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения данных пользователей: {e}")
    
    def get_or_create_user(self, user_id: int, username: str = None, first_name: str = None) -> Dict:
        """Получает или создает пользователя"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.users:
            self.users[user_id_str] = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_date": datetime.now().isoformat(),
                "requests": {
                    "total": 0,
                    "today": 0,
                    "week": 0,
                    "last_request": None
                },
                "requests_history": []
            }
            self.save_users()
        
        return self.users[user_id_str]
    
    def record_request(self, user_id: int, request_type: str):
        """Записывает запрос пользователя"""
        user_id_str = str(user_id)
        now = datetime.now()
        
        if user_id_str not in self.users:
            return
        
        user = self.users[user_id_str]
        
        # Обновляем общую статистику
        user["requests"]["total"] += 1
        user["requests"]["last_request"] = now.isoformat()
        
        # Добавляем в историю
        user["requests_history"].append({
            "type": request_type,
            "timestamp": now.isoformat()
        })
        
        # Ограничиваем историю последними 100 запросами
        if len(user["requests_history"]) > 100:
            user["requests_history"] = user["requests_history"][-100:]
        
        # Обновляем дневную и недельную статистику
        self.update_period_stats(user_id_str)
        
        self.save_users()
    
    def update_period_stats(self, user_id_str: str):
        """Обновляет дневную и недельную статистику"""
        user = self.users[user_id_str]
        now = datetime.now()
        
        # Сбрасываем счетчики
        user["requests"]["today"] = 0
        user["requests"]["week"] = 0
        
        # Подсчитываем запросы за день и неделю
        for request in user["requests_history"]:
            request_time = datetime.fromisoformat(request["timestamp"])
            
            if now.date() == request_time.date():
                user["requests"]["today"] += 1
            
            if now - request_time <= timedelta(days=7):
                user["requests"]["week"] += 1
    
    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь админом"""
        return user_id in self.admins
    
    def get_stats(self) -> Dict:
        """Получает общую статистику по всем пользователям"""
        try:
            total_users = len(self.users)
            total_requests = 0
            today_requests = 0
            week_requests = 0
            
            # Безопасно подсчитываем статистику
            for user in self.users.values():
                try:
                    requests = user.get("requests", {})
                    total_requests += requests.get("total", 0)
                    today_requests += requests.get("today", 0)
                    week_requests += requests.get("week", 0)
                except Exception as e:
                    logger.error(f"Ошибка при обработке пользователя {user.get('user_id', 'unknown')}: {e}")
                    continue
            
            # Топ пользователей по запросам
            try:
                top_users = sorted(
                    self.users.values(),
                    key=lambda x: x.get("requests", {}).get("total", 0),
                    reverse=True
                )[:5]
            except Exception as e:
                logger.error(f"Ошибка при сортировке пользователей: {e}")
                top_users = []
            
            return {
                "total_users": total_users,
                "total_requests": total_requests,
                "today_requests": today_requests,
                "week_requests": week_requests,
                "top_users": top_users
            }
        except Exception as e:
            logger.error(f"Ошибка в get_stats: {e}")
            return {
                "total_users": 0,
                "total_requests": 0,
                "today_requests": 0,
                "week_requests": 0,
                "top_users": []
            }
    
    def get_user_stats(self, user_id: int) -> Optional[Dict]:
        """Получает статистику конкретного пользователя"""
        user_id_str = str(user_id)
        if user_id_str in self.users:
            self.update_period_stats(user_id_str)
            return self.users[user_id_str]
        return None 