#!/usr/bin/env python3
"""
Переопубликация статьи с правильной ссылкой в заголовке.
"""

import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
import requests
import json

def escape_markdown_v2(text):
    """
    Экранировать специальные символы для Telegram Markdown V2.
    """
    chars_to_escape = r'_*[]()~`>#+-=|{}.!'
    for char in chars_to_escape:
        text = text.replace(char, f'\\{char}')
    return text

ARTICLE_TITLE = "10 ситуаций, где ИИ уже работает: практическое руководство"
TELEGRAM_EMOJI = "🤖"
HASHTAGS = "#ai #технологии #практика #нейросети"

ARTICLE_CONTENT = """Искусственный интеллект перестал быть технологией будущего. Он уже здесь. Разобрали 10 практических ситуаций, где нейросети экономят время, деньги и нервы.

## 1. Написание текстов и контента

**Задача:** Создать статью.

**Как помогает ИИ:**

- Генерирует черновики
- Предлагает варианты

**Инструменты:** ChatGPT, Claude

## 2. Поиск информации

**Задача:** Найти данные.

**Как помогает ИИ:**

- Обрабатывает источники
- Выделяет факты

**Инструменты:** Perplexity, Consensus

---

Полная версия: 10 разделов с инструментами и примерами.

Источники: MIT Technology Review, Stanford HAI, Harvard Business Review
"""

print("📝 Переопубликация статьи с правильной ссылкой...")

config = json.load(open('/root/git/AI-journalist-bot/telegraph_config.json'))
access_token = config.get('access_token')

content_nodes = create_telegraph_content(ARTICLE_CONTENT, include_title=False)

url = "https://api.telegra.ph/createPage"
data = {
    "access_token": access_token,
    "title": ARTICLE_TITLE,
    "content": json.dumps(content_nodes),
    "return_content": False
}

response = requests.post(url, json=data)
result = response.json()

if result.get("ok"):
    article_url = result["result"]["url"]
    print(f"✅ Статья опубликована!")
    print(f"📰 URL: {article_url}")
    
    # Экранируем URL для Telegram Markdown V2
    escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
    
    # Описание экранируем полностью
    description = """Практическое руководство по применению нейросетей: от написания текстов до анализа данных.

Разбираем инструменты, возможности и ограничения."""
    escaped_description = escape_markdown_v2(description)
    
    # Хэштеги экранируем
    escaped_hashtags = HASHTAGS.replace('#', '\\#')
    
    announcement = f"""{TELEGRAM_EMOJI} [{ARTICLE_TITLE}]({escaped_url})

{escaped_description}

{escaped_hashtags}"""
    
    print("\n📢 Анонс для публикации:")
    print("-" * 40)
    print(announcement)
    print("-" * 40)
    
    print("\n📢 Публикация анонса в Telegram...")
    
    config = json.load(open('/root/git/AI-journalist-bot/config.json'))
    token = config['token']
    channel_id = config['channel_id']
    
    tg_url = f'https://api.telegram.org/bot{token}/sendMessage'
    tg_data = {
        'chat_id': channel_id,
        'text': announcement,
        'parse_mode': 'MarkdownV2'
    }
    
    tg_result = requests.post(tg_url, json=tg_data)
    tg_result_json = tg_result.json()
    
    if tg_result_json.get('ok'):
        msg_id = tg_result_json['result']['message_id']
        print(f"✅ Анонс опубликован! Message ID: {msg_id}")
    else:
        print(f"❌ Ошибка: {tg_result_json.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка публикации: {error}")
