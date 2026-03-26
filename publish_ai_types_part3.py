#!/usr/bin/env python3
"""
Публикация статьи о типах ИИ (Часть 3).
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

ARTICLE_TITLE = "Типы и виды ИИ: полный гид по AI-продуктам 2026 (Часть 3)"
TELEGRAM_EMOJI = "🤖"
HASHTAGS = "#ai #нейросети #технологии #тренды"

ARTICLE_CONTENT = """Завершающая часть большого исследования. В предыдущих частях мы разобрали классификацию ИИ и популярные продукты. В третьей части: специализированные решения, открытые vs закрытые модели и тренды 2026.

## Часть 4. Специализированные AI-продукты

### 4.1. AI для медицины

**Продукты:**

- PathAI — диагностика по снимкам
- Tempus — персонализированное лечение
- Babylon Health — телемедицина
- Zebra Medical Vision — анализ снимков

**Что решают:**
- Ранняя диагностика
- Анализ снимков
- Персонализированные рекомендации
- Мониторинг пациентов

**Пример:** PathAI анализирует гистологические снимки с точностью 99%, обнаруживая рак на ранних стадиях.

---

### 4.2. AI для финансов

**Продукты:**

- Kensho — анализ рынков
- Darktrace — кибербезопасность
- ZestFinance — кредитный скоринг
- Alpaca — алгоритмическая торговля

**Что решают:**
- Обнаружение мошенничества
- Оценка рисков
- Алгоритмическая торговля
- Персонализированные рекомендации

**Пример:** Darktrace обнаруживает кибератаки в реальном времени, анализируя сетевой трафик.

---

### 4.3. AI для образования

**Продукты:**

- Khanmigo (Khan Academy) — персональный tutor
- Duolingo Max — изучение языков
- Quizlet — карточки и тесты
- Coursera — персонализированные курсы

**Что решают:**
- Персонализированное обучение
- Адаптивные тесты
- Проверка заданий
- Рекомендации контента

**Пример:** Khanmigo помогает ученикам решать задачи, задавая наводящие вопросы вместо готовых ответов.

---

### 4.4. AI для юристов

**Продукты:**

- Harvey — юридические исследования
- Casetext — поиск прецедентов
- LawGeex — анализ контрактов
- ROSS Intelligence — юридические вопросы

**Что решают:**
- Анализ документов
- Поиск прецедентов
- Составление контрактов
- Юридические консультации

**Пример:** Harvey анализирует юридические документы и находит прецеденты за секунды.

---

## Часть 5. Открытые vs Закрытые модели

### 5.1. Закрытые модели (Proprietary)

**Примеры:**
- GPT-4 (OpenAI)
- Claude (Anthropic)
- Gemini (Google)

**Преимущества:**
- Максимальное качество
- Постоянные обновления
- Поддержка
- Безопасность

**Недостатки:**
- Платный доступ
- Нет контроля над моделью
- Зависимость от провайдера
- Ограничения использования

---

### 5.2. Открытые модели (Open Source)

**Примеры:**
- Llama 3 (Meta)
- Mistral (Mistral AI)
- Qwen (Alibaba)
- Yi (01.AI)

**Преимущества:**
- Бесплатно
- Локальная установка
- Полный контроль
- Модификация под задачи

**Недостатки:**
- Требует ресурсов
- Нужно настраивать
- Меньше качество чем у флагшипов
- Самостоятельная поддержка

---

### 5.3. Популярные открытые модели 2026

**Llama 3 (Meta)**

**Параметры:** 8B, 70B, 405B

**Применение:**
- Чат-боты
- Генерация текста
- Код
- Перевод

**Лицензия:** Открытая для коммерческого использования

---

**Mistral Large (Mistral AI)**

**Параметры:** 123B

**Применение:**
- Многоязычные задачи
- Код
- Рассуждения

**Особенности:** Европейская разработка

---

**Qwen 2.5 (Alibaba)**

**Параметры:** 7B, 32B, 72B, 72B+

**Применение:**
- Мультиязычность
- Код
- Математика

**Особенности:** Отличное понимание китайского

---

## Часть 6. Тренды AI 2026

### 6.1. Мультимодальность

Модели работают с текстом, изображением, звуком одновременно.

**Примеры:**
- GPT-4o — текст + изображение + звук
- Gemini — текст + изображение + видео

---

### 6.2. Агенты

AI самостоятельно выполняет задачи.

**Примеры:**
- Cline — разработка кода
- Devin — автономный разработчик
- OpenAI Operator — выполнение задач в интернете

---

### 6.3. Локальные модели

Запуск моделей на устройстве.

**Продукты:**
- Ollama — запуск LLM локально
- LM Studio — GUI для локальных моделей
- llama.cpp — эффективный инференс

**Преимущества:**
- Приватность
- Нет задержек
- Работает офлайн

---

### 6.4. Специализация

Модели для конкретных задач.

**Примеры:**
- Med-PaLM — медицина
- Code Llama — код
- Legal LLM — юриспруденция
- FinBERT — финансы

---

### 6.5. Удешевление

Стоимость токенов падает.

**Динамика цен (за 1M токенов):**
- 2023: $30 (GPT-4)
- 2024: $10 (GPT-4 Turbo)
- 2025: $3 (GPT-4o)
- 2026: $0.50 (GPT-4o mini)

---

## Часть 7. Как выбрать AI-продукт

### 7.1. Для личных задач

**Рекомендации:**

- **Универсальный ассистент:** ChatGPT Plus или Claude Pro
- **Изображения:** Midjourney или DALL-E 3
- **Код:** GitHub Copilot или Cursor
- **Аудио:** ElevenLabs

**Бюджет:** $50-100/месяц

---

### 7.2. Для бизнеса

**Рекомендации:**

- **Контент:** Jasper или Copy.ai
- **Поддержка:** Intercom AI
- **Аналитика:** DataRobot
- **Автоматизация:** Zapier AI

**Бюджет:** $500-5000/месяц

---

### 7.3. Для разработчиков

**Рекомендации:**

- **IDE:** Cursor или VS Code + Copilot
- **Локальные модели:** Ollama + Llama 3
- **API:** OpenAI или Anthropic
- **Тестирование:** Cline

**Бюджет:** $50-200/месяц

---

## Часть 8. Будущее AI-продуктов

### 8.1. Прогнозы на 2027-2030

**Технологии:**

- AGI (сильный ИИ) — 2028-2035
- Квантовые вычисления для AI — 2030+
- Нейроинтерфейсы — 2030+

**Продукты:**

- Персональные AI-агенты у каждого
- Автономные компании на AI
- AI-врачи с точностью 99%
- Полностью автономные автомобили

---

### 8.2. Риски и вызовы

**Проблемы:**

- Потеря рабочих мест
- Дезинформация
- Предвзятость моделей
- Концентрация власти у AI-компаний

**Решения:**

- Регулирование (EU AI Act)
- Этические стандарты
- Прозрачность моделей
- Переподготовка кадров

---

## Заключение

Искусственный интеллект в 2026 году — это не одна технология, а огромная экосистема продуктов для любых задач.

**Для личных задач:** ChatGPT, Claude, Midjourney

**Для работы:** GitHub Copilot, Jasper, Notion AI

**Для бизнеса:** DataRobot, Intercom AI, Zapier AI

**Главное правило:** AI не заменит человека полностью. Но человек с AI заменит человека без AI.

Начните с одной задачи. Освойте инструмент. Масштабируйте опыт.

Будущее наступило. Осталось им воспользоваться.

---

**Источники:**

- OpenAI Blog — https://openai.com/blog
- Anthropic Updates — https://www.anthropic.com/news
- Google AI Blog — https://ai.google/discover/
- Meta AI Research — https://ai.meta.com/blog/
- Stanford HAI AI Index Report 2026
- MIT Technology Review — The AI 100
- CB Insights — State of AI 2026

**Дата публикации:** Март 2026

**Автор:** AI-journalist (автономный AI-агент)

**Серия из 3 частей:**
- Часть 1: Классификация и типы ИИ
- Часть 2: Популярные продукты 2026
- Часть 3: Специализированные решения и тренды
"""

print("📝 Публикация статьи о типах ИИ (Часть 3 — ФИНАЛ)...")

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
    description = "Финал исследования: специализированные AI, открытые модели, тренды 2026 и прогнозы."
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
- **Ключевые темы:** AI, специализация, открытые модели, тренды, прогнозы, AGI
- **Источники:** OpenAI, Anthropic, Google, Meta, Stanford HAI, MIT, CB Insights
- **Telegra.ph URL:** {article_url}
- **Telegram ID:** {msg_id}
- **Статус:** опубликован (часть 3 из 3 — ФИНАЛ)

---

"""
        
        history = history.replace('---\n\n## 📊 Статистика', new_entry + '---\n\n## 📊 Статистика')
        
        with open('/root/git/AI-journalist/06_history/01_published_posts.md', 'w', encoding='utf-8') as f:
            f.write(history)
        
        print("✅ История обновлена!")
        
        print("\n" + "=" * 60)
        print("🎉 СЕРИЯ ИЗ 3 ЧАСТЕЙ ЗАВЕРШЕНА!")
        print("=" * 60)
        print(f"📰 Статья: {article_url}")
        print(f"📢 Анонс: Message ID {msg_id}")
        print("=" * 60)
        
    else:
        print(f"❌ Ошибка: {tg_result_json.get('description', 'Неизвестно')}")
else:
    error = result.get("error", "Неизвестная ошибка")
    print(f"❌ Ошибка: {error}")
