#!/usr/bin/env python3
"""
Тестовая публикация с таблицей для проверки форматирования.
"""

import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
import requests
import json

def escape_markdown_v2(text):
    chars_to_escape = r'_*[]()~`>#+-=|{}.!'
    for char in chars_to_escape:
        text = text.replace(char, f'\\{char}')
    return text

ARTICLE_TITLE = "Тест форматирования: Таблицы и списки"
TELEGRAM_EMOJI = "🧪"
HASHTAGS = "#тест #форматирование"

ARTICLE_CONTENT = """Тестируем новое форматирование для Telegraph.

## Таблицы

| Критерий | ChatGPT | Claude | Gemini |
|----------|---------|--------|--------|
| Качество | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Скорость | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Контекст | 128K | 200K | 1M+ |
| Цена | $20 | $20 | $20 |

## Списки

**Преимущества:**

- Высокое качество
- Быстрая работа
- Надёжность

**Недостатки:**

- Платный доступ
- Ограничения

## Форматирование текста

Это **жирный текст** и _курсив_ и `код`.

Ссылка: [Google](https://google.com)

---

Таблица выше должна отображаться как текст с маркерами •
"""

print("📝 Тестовая публикация...")

config = json.load(open('/root/git/AI-journalist-bot/telegraph_config.json'))
access_token = config.get('access_token')

content_nodes = create_telegraph_content(ARTICLE_CONTENT, include_title=False)

# Выводим JSON для отладки
print("\n📄 JSON контент (первые 1000 символов):")
print(json.dumps(content_nodes[:5], indent=2, ensure_ascii=False)[:1000])

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
    print(f"\n✅ Опубликовано: {article_url}")
    
    # Отправляем URL пользователю в бота
    print(f"\n📤 Отправьте ссылку пользователю: {article_url}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"\n❌ Ошибка: {error}")
