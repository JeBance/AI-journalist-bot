#!/usr/bin/env python3
"""
Переопубликация второй статьи с исправленным форматированием.
"""

import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
from publisher import publish
import requests
import json

# Импортируем статью из publish_second_article.py
exec(open('/root/git/AI-journalist-bot/publish_second_article.py').read().split('print(')[0])

print("📝 Переопубликация второй статьи с исправленным форматированием...")

# Загружаем конфиг
config = json.load(open('/root/git/AI-journalist-bot/telegraph_config.json'))
access_token = config.get('access_token')

# Конвертируем контент
content_nodes = create_telegraph_content(article_content)

# Публикуем
url = "https://api.telegra.ph/createPage"
data = {
    "access_token": access_token,
    "title": "10 ситуаций, где ИИ уже работает: практическое руководство",
    "content": json.dumps(content_nodes),
    "return_content": False
}

response = requests.post(url, json=data)
result = response.json()

if result.get("ok"):
    article_url = result["result"]["url"]
    print(f"✅ Статья опубликована!")
    print(f"📰 URL: {article_url}")
    
    # Создаём анонс
    announcement = f"""📖 <b>Новая статья на Telegra.ph</b>

<b>10 ситуаций, где ИИ уже работает</b>

Практическое руководство по применению нейросетей:

- Написание текстов
- Программирование
- Обработка изображений
- Перевод и обучение
- Анализ данных и не только

<a href="{article_url}">Читать статью →</a>

#ai #технологии #практика #нейросети"""
    
    print("\n📢 Публикация анонса в Telegram...")
    
    config = json.load(open('/root/git/AI-journalist-bot/config.json'))
    token = config['token']
    channel_id = config['channel_id']
    
    tg_url = f'https://api.telegram.org/bot{token}/sendMessage'
    tg_data = {
        'chat_id': channel_id,
        'text': announcement,
        'parse_mode': 'HTML'
    }
    
    tg_result = requests.post(tg_url, json=tg_data).json()
    
    if tg_result.get('ok'):
        print(f"✅ Анонс опубликован! Message ID: {tg_result['result']['message_id']}")
    else:
        print(f"❌ Ошибка публикации анонса: {tg_result.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка публикации: {error}")
