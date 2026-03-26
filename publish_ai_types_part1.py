#!/usr/bin/env python3
"""
Публикация статьи о типах ИИ (Часть 1).
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

ARTICLE_TITLE = "Типы и виды ИИ: полный гид по AI-продуктам 2026 (Часть 1)"
TELEGRAM_EMOJI = "🤖"
HASHTAGS = "#ai #нейросети #технологии #обзор"

ARTICLE_CONTENT = """Искусственный интеллект перестал быть единой технологией. Сегодня это огромная экосистема из десятков направлений, продуктов и сервисов. Разбираемся в типах ИИ и смотрим, что уже работает в 2026 году.

## Часть 1. Классификация ИИ по возможностям

### 1.1. Слабый ИИ (ANI — Artificial Narrow Intelligence)

Специализированный интеллект для решения конкретных задач.

**Что умеет:**

- Распознавание изображений и речи
- Перевод текстов
- Рекомендации контента
- Игра в шахматы и го

**Примеры:**

- Siri, Alexa, Google Assistant
- ChatGPT, Claude, Gemini
- Midjourney, DALL-E 3
- Системы рекомендаций Netflix, YouTube

**Ограничения:** Не может решать задачи вне своей специализации.

### 1.2. Сильный ИИ (AGI — Artificial General Intelligence)

Гипотетический интеллект, способный решать любые интеллектуальные задачи человека.

**Статус 2026:** Не существует в полной мере.

**Ближайшие попытки:**

- GPT-4o — мультимодальность (текст, изображение, звук)
- Claude 3.5 — рассуждения и планирование
- Gemini Ultra — интеграция с инструментами

**Прогноз экспертов:** 2028-2035 годы.

### 1.3. Искусственный суперинтеллект (ASI)

Интеллект, превосходящий человеческий во всех областях.

**Статус 2026:** Теоретическая концепция.

**Риски:**

- Потеря контроля
- Этические вопросы
- Влияние на рынок труда

---

## Часть 2. Типы ИИ по функционалу

### 2.1. Генеративный ИИ (Generative AI)

Создаёт новый контент: текст, изображения, код, музыку.

**Популярные продукты:**

**Текст:**

- ChatGPT (OpenAI) — универсальный ассистент
- Claude (Anthropic) — анализ документов, код
- Gemini (Google) — интеграция с сервисами Google
- Qwen (Alibaba) — мультиязычность

**Изображения:**

- Midjourney — художественные изображения
- DALL-E 3 (OpenAI) — точное следование промпту
- Stable Diffusion — открытый, локальная установка
- Adobe Firefly — коммерческое использование

**Код:**

- GitHub Copilot — автодополнение кода
- Cursor — AI-first IDE
- Cline — автономный агент для разработки
- Continue — open-source альтернатива

**Видео:**

- Sora (OpenAI) — генерация видео по тексту
- Runway Gen-2 — редактирование видео
- Pika Labs — анимация изображений

**Аудио:**

- ElevenLabs — синтез речи
- Suno AI — генерация музыки
- Udio — песни по промпту

### 2.2. Предиктивный ИИ (Predictive AI)

Прогнозирует будущие события на основе данных.

**Применение:**

- Прогноз погоды
- Предсказание спроса
- Оценка кредитных рисков
- Прогнозирование отказов оборудования

**Продукты:**

- Prophet (Meta) — прогнозирование временных рядов
- DataRobot — автоматическое ML
- H2O.ai — предиктивная аналитика
- Amazon Forecast — облачные прогнозы

### 2.3. Распознающий ИИ (Recognition AI)

Распознаёт образы: изображения, речь, текст.

**Применение:**

- Распознавание лиц
- Транскрибация речи
- Оптический распознавание символов (OCR)
- Медицинская диагностика

**Продукты:**

- Google Cloud Vision — анализ изображений
- AWS Rekognition — распознавание лиц
- Whisper (OpenAI) — транскрибация речи
- Tesseract — открытый OCR

### 2.4. Рекомендательный ИИ (Recommendation AI)

Предлагает контент на основе предпочтений.

**Где используется:**

- Netflix — рекомендации фильмов
- YouTube — рекомендации видео
- Spotify — музыкальные плейлисты
- Amazon — товары

**Технологии:**

- Коллаборативная фильтрация
- Контентная фильтрация
- Гибридные системы

### 2.5. Робототехнический ИИ (Robotics AI)

Управляет физическими устройствами.

**Применение:**

- Автономные автомобили
- Промышленные роботы
- Дроны
- Роботы-пылесосы

**Продукты:**

- Tesla Autopilot — автономное вождение
- Boston Dynamics — роботы-гуманоиды
- iRobot — бытовые роботы
- NVIDIA Isaac — платформа для роботов

---

**Продолжение следует...**

Во второй части: популярные AI-продукты 2026, специализированные решения и тренды.

**Источники:**

- OpenAI Blog
- Anthropic Updates
- Google AI Blog
- Stanford HAI AI Index Report 2026
- MIT Technology Review

**Дата:** Март 2026
"""

print("📝 Публикация статьи о типах ИИ (Часть 1)...")

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
    
    escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
    description = "Большое исследование: классификация ИИ по возможностям и функционалу. Генеративный, предиктивный, распознающий ИИ — разбираем популярные продукты."
    escaped_description = escape_markdown_v2(description)
    escaped_hashtags = HASHTAGS.replace('#', '\\#')
    
    # Заголовок тоже нужно экранировать полностью
    escaped_title = escape_markdown_v2(ARTICLE_TITLE)
    
    announcement = f"""{TELEGRAM_EMOJI} [{escaped_title}]({escaped_url})

{escaped_description}

{escaped_hashtags}"""
    
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
        
        # Запись в историю
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        with open('/root/git/AI-journalist/06_history/01_published_posts.md', 'r', encoding='utf-8') as f:
            history = f.read()
        
        new_entry = f"""### [{today}] {ARTICLE_TITLE}

- **Категория:** ai_tools
- **Шаблон:** telegra.ph article (серия из 3 частей)
- **Ключевые темы:** AI, типы ИИ, классификация, генеративный ИИ, продукты
- **Источники:** OpenAI, Anthropic, Google, Stanford HAI, MIT
- **Telegra.ph URL:** {article_url}
- **Telegram ID:** {msg_id}
- **Статус:** опубликован (часть 1 из 3)

---

"""
        
        history = history.replace('---\n\n## 📊 Статистика', new_entry + '---\n\n## 📊 Статистика')
        
        with open('/root/git/AI-journalist/06_history/01_published_posts.md', 'w', encoding='utf-8') as f:
            f.write(history)
        
        print("✅ История обновлена!")
        print(f"\n🔗 Продолжение: Часть 2 будет опубликована отдельно")
        
    else:
        print(f"❌ Ошибка: {tg_result_json.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка: {error}")
