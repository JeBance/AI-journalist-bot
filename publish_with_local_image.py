#!/usr/bin/env python3
"""
Публикация статьи с изображением (загрузка файлом).
"""

import sys
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
from find_free_image import get_image_for_article
import requests
import json
import tempfile
import os

# Содержимое статьи
article_content = """# 10 ситуаций, где ИИ уже работает: практическое руководство

Искусственный интеллект перестал быть технологией будущего. Он уже здесь. Разобрали 10 практических ситуаций, где нейросети экономят время, деньги и нервы.

## 1. Написание текстов и контента

**Задача:** Создать статью, пост для соцсетей, письмо или документ.

**Как помогает ИИ:**

- Генерирует черновики за секунды
- Предлагает варианты заголовков
- Проверяет грамматику и стиль
- Адаптирует текст под аудиторию

**Инструменты:** ChatGPT, Claude, Gemini, Qwen

## 2. Поиск и анализ информации

**Как помогает ИИ:**

- Обрабатывает сотни источников одновременно
- Выделяет ключевые факты
- Сравнивает разные точки зрения

**Инструменты:** Perplexity, Consensus, Elicit

## 3. Программирование и код

**Как помогает ИИ:**

- Генерирует код по описанию
- Находит баги и уязвимости
- Пишет тесты и документацию

**Инструменты:** GitHub Copilot, Cursor, Cline

## 4. Обработка изображений

**Инструменты:** Midjourney, DALL-E 3, Stable Diffusion

## 5. Перевод и локализация

**Инструменты:** DeepL, Google Translate

## 6. Обучение и образование

**Инструменты:** Khanmigo, Duolingo Max

## 7. Планирование и организация

**Инструменты:** Reclaim.ai, Motion

## 8. Анализ данных

**Инструменты:** Julius AI, Tableau AI

## 9. Поддержка клиентов

**Инструменты:** Intercom AI, Zendesk AI

## 10. Здоровье и фитнес

**Инструменты:** Fitbit AI, MyFitnessPal

## Заключение

ИИ не заменит человека полностью. Но человек с ИИ заменит человека без ИИ.

---

Полная версия: https://telegra.ph

Источники: MIT Technology Review, Stanford HAI, Harvard Business Review
"""

print("📝 Публикация статьи на Telegra.ph...")

# Загружаем конфиг
config = json.load(open('/root/git/AI-journalist-bot/telegraph_config.json'))
access_token = config.get('access_token')

# Конвертируем контент
content_nodes = create_telegraph_content(article_content)

# Публикуем
url = "https://api.telegra.ph/createPage"
data = {
    "access_token": access_token,
    "title": "10 ситуаций, где ИИ уже работает",
    "content": json.dumps(content_nodes),
    "return_content": False
}

response = requests.post(url, json=data)
result = response.json()

if result.get("ok"):
    article_url = result["result"]["url"]
    print(f"✅ Статья опубликована!")
    print(f"📰 URL: {article_url}")
    
    # Находим изображение
    print("\n🖼️ Загрузка изображения...")
    image_url = get_image_for_article("AI")
    
    # Скачиваем изображение во временный файл
    img_response = requests.get(image_url)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
        f.write(img_response.content)
        temp_image_path = f.name
    
    print(f"   Изображение сохранено: {temp_image_path}")
    
    # Создаём упрощённый анонс
    announcement = f"""🤖 10 ситуаций, где ИИ уже работает

Практическое руководство по применению нейросетей: от написания текстов до анализа данных.

Разбираем инструменты, возможности и ограничения.

Читать: {article_url}

#ai #технологии #практика"""
    
    # Публикуем с изображением файлом
    print("\n📢 Публикация анонса с изображением...")
    
    config = json.load(open('/root/git/AI-journalist-bot/config.json'))
    token = config['token']
    channel_id = config['channel_id']
    
    tg_url = f'https://api.telegram.org/bot{token}/sendPhoto'
    
    with open(temp_image_path, 'rb') as photo:
        tg_data = {
            'chat_id': channel_id,
            'caption': announcement
        }
        files = {'photo': photo}
        
        tg_result = requests.post(tg_url, data=tg_data, files=files)
    
    tg_result_json = tg_result.json()
    
    # Удаляем временный файл
    os.unlink(temp_image_path)
    
    if tg_result_json.get('ok'):
        msg_id = tg_result_json['result']['message_id']
        print(f"✅ Анонс с изображением опубликован! Message ID: {msg_id}")
    else:
        print(f"❌ Ошибка: {tg_result_json.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка публикации: {error}")
