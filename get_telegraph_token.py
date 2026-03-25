#!/usr/bin/env python3
"""
Получение токена доступа Telegra.ph
"""

import requests
import json
import random

# URL API
url = "https://api.telegra.ph/createAccount"

# Генерируем имя автора
short_name = "AI Journalist"
author_name = "AI Journalist"
author_url = "https://t.me/JeBanceOnline"

data = {
    "short_name": short_name,
    "author_name": author_name,
    "author_url": author_url
}

print("📝 Регистрация аккаунта на Telegra.ph...")
print(f"Short name: {short_name}")
print(f"Author: {author_name}")

response = requests.post(url, json=data)
result = response.json()

if result.get("ok"):
    access_token = result["result"]["access_token"]
    print(f"\n✅ Аккаунт создан!")
    print(f"🔑 Access Token: {access_token}")
    print(f"\n📁 Сохраните токен в telegraph_config.json:")
    
    config = {
        "access_token": access_token,
        "short_name": short_name,
        "author_name": author_name,
        "author_url": author_url
    }
    
    print(json.dumps(config, indent=2))
    
    # Сохраняем в файл
    config_file = "/root/git/AI-journalist-bot/telegraph_config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n💾 Токен сохранён в {config_file}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка: {error}")
