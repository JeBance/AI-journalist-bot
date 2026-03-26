#!/usr/bin/env python3
"""
Публикация статьи о типах ИИ (Часть 2).
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

ARTICLE_TITLE = "Типы и виды ИИ: полный гид по AI-продуктам 2026 (Часть 2)"
TELEGRAM_EMOJI = "🤖"
HASHTAGS = "#ai #нейросети #технологии #обзор"

ARTICLE_CONTENT = """Продолжение большого исследования современных AI-продуктов. В первой части мы разобрали классификацию ИИ. Во второй части смотрим на популярные продукты 2026 года.

## Часть 3. Популярные AI-продукты 2026

### 3.1. Универсальные ассистенты

**ChatGPT (OpenAI)**

**Что решает:**
- Написание текстов и кода
- Анализ документов
- Обучение и объяснения
- Автоматизация задач

**Аудитория:** 200+ млн пользователей

**Модели:**
- GPT-4o — флагшип
- GPT-4o mini — быстрая и дешёвая
- o1 — рассуждения и математика

**Цена:** $20/месяц (Plus)

---

**Claude (Anthropic)**

**Что решает:**
- Анализ больших документов (200K токенов)
- Написание кода
- Безопасные ответы
- Долгий контекст

**Аудитория:** Разработчики, аналитики

**Модели:**
- Claude 3.5 Sonnet — баланс скорости и качества
- Claude 3.5 Opus — максимальные возможности
- Claude 3.5 Haiku — быстрый и дешёвый

**Цена:** $20/месяц (Pro)

---

**Gemini (Google)**

**Что решает:**
- Интеграция с Google сервисами
- Мультимодальный анализ
- Поиск информации
- Планирование

**Аудитория:** Пользователи экосистемы Google

**Модели:**
- Gemini 2.0 Pro — флагшип
- Gemini 2.0 Flash — быстрый
- Gemini 2.0 Nano — на устройстве

**Цена:** $20/месяц (Advanced)

---

### 3.2. AI для разработки

**GitHub Copilot**

**Что решает:**
- Автодополнение кода
- Генерация функций по описанию
- Рефакторинг
- Написание тестов

**Поддерживаемые языки:** Python, JavaScript, TypeScript, Java, C++, Go, PHP, Ruby

**Интеграции:** VS Code, JetBrains, Neovim, Visual Studio

**Цена:** $10/месяц

---

**Cursor**

**Что решает:**
- AI-first IDE
- Редактирование кода через чат
- Поиск по кодовой базе
- Автоисправление ошибок

**Особенности:**
- Основан на VS Code
- Локальная обработка кода
- Интеграция с GitHub

**Цена:** $20/месяц (Pro)

---

**Cline**

**Что решает:**
- Автономное выполнение задач
- Работа с терминалом
- Создание файлов
- Отладка кода

**Особенности:**
- Open-source
- Работает локально
- Использует любую LLM

**Цена:** Бесплатно

---

### 3.3. AI для дизайна и изображений

**Midjourney**

**Что решает:**
- Генерация художественных изображений
- Концепт-арт
- Иллюстрации
- Логотипы

**Особенности:**
- Высокое качество
- Художественный стиль
- Работа через Discord

**Цена:** $10-120/месяц

---

**DALL-E 3 (OpenAI)**

**Что решает:**
- Генерация изображений по тексту
- Редактирование изображений
- Вариации изображений

**Особенности:**
- Точное следование промпту
- Интеграция с ChatGPT
- Безопасность контента

**Цена:** Через ChatGPT Plus ($20/месяц)

---

**Stable Diffusion**

**Что решает:**
- Генерация изображений
- Редактирование
- Inpainting/outpainting
- ControlNet для контроля позы

**Особенности:**
- Открытая модель
- Локальная установка
- Тысячи финетюнов

**Цена:** Бесплатно

---

### 3.4. AI для видео

**Sora (OpenAI)**

**Что решает:**
- Генерация видео по тексту
- Редактирование видео
- Анимация изображений

**Статус 2026:** Ограниченный доступ

**Особенности:**
- До 60 секунд видео
- Высокое качество
- Понимание физики

---

**Runway Gen-2**

**Что решает:**
- Генерация видео
- Редактирование
- Удаление объектов
- Замена фона

**Цена:** $12-95/месяц

---

### 3.5. AI для аудио

**ElevenLabs**

**Что решает:**
- Синтез речи из текста
- Клонирование голоса
- Перевод с сохранением голоса
- Генерация звуковых эффектов

**Применение:**
- Озвучка видео
- Аудиокниги
- Подкасты
- Игры

**Цена:** $5-330/месяц

---

**Suno AI**

**Что решает:**
- Генерация музыки по тексту
- Создание песен с вокалом
- Разные жанры и стили

**Особенности:**
- Полные песни (куплет, припев)
- Текст и музыка одновременно
- Высокое качество

**Цена:** $10-30/месяц

---

### 3.6. AI для бизнеса

**Jasper**

**Что решает:**
- Маркетинговые тексты
- Контент для соцсетей
- Email-рассылки
- Рекламные объявления

**Аудитория:** Маркетологи, контент-менеджеры

**Цена:** $49-125/месяц

---

**Notion AI**

**Что решает:**
- Саммаризация заметок
- Генерация контента
- Перевод
- Улучшение текста

**Интеграция:** Встроен в Notion

**Цена:** $10/месяц

---

**Grammarly**

**Что решает:**
- Проверка грамматики
- Улучшение стиля
- Тон письма
- Плагиат

**Аудитория:** 30+ млн пользователей

**Цена:** $12-30/месяц

---

**Продолжение следует...**

В третьей части: специализированные AI-продукты для медицины, финансов, образования и права. Открытые vs закрытые модели. Тренды 2026.

**Источники:**

- OpenAI Blog
- Anthropic Updates
- Google AI Blog
- Meta AI Research
- Stanford HAI AI Index Report 2026
- MIT Technology Review
- CB Insights — State of AI 2026

**Дата:** Март 2026
"""

print("📝 Публикация статьи о типах ИИ (Часть 2)...")

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
    print(f"\n✅ Статья опубликована!")
    print(f"📰 URL: {article_url}")
    
    escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
    description = "Популярные AI-продукты 2026: ChatGPT, Claude, Gemini, GitHub Copilot, Midjourney, ElevenLabs."
    escaped_description = escape_markdown_v2(description)
    escaped_hashtags = HASHTAGS.replace('#', '\\#')
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
- **Ключевые темы:** AI, продукты 2026, ChatGPT, Claude, Midjourney, GitHub Copilot
- **Источники:** OpenAI, Anthropic, Google, Meta, Stanford HAI, MIT, CB Insights
- **Telegra.ph URL:** {article_url}
- **Telegram ID:** {msg_id}
- **Статус:** опубликован (часть 2 из 3)

---

"""
        
        history = history.replace('---\n\n## 📊 Статистика', new_entry + '---\n\n## 📊 Статистика')
        
        with open('/root/git/AI-journalist/06_history/01_published_posts.md', 'w', encoding='utf-8') as f:
            f.write(history)
        
        print("✅ История обновлена!")
        print(f"\n🔗 Продолжение: Часть 3 будет опубликована отдельно")
        
    else:
        print(f"❌ Ошибка: {tg_result_json.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка: {error}")
