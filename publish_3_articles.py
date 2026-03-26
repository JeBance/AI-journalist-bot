#!/usr/bin/env python3
"""
Публикация 3 статей подряд.
"""

import sys
import json
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
import requests

def escape_markdown_v2(text):
    chars_to_escape = r'_*[]()~`>#+-=|{}.!'
    for char in chars_to_escape:
        text = text.replace(char, f'\\{char}')
    return text

def publish_article(title, content, emoji, hashtags):
    """Публикация одной статьи."""
    print(f"\n📝 Публикация: {title}")
    
    # Загружаем конфиг
    config = json.load(open('/root/git/AI-journalist-bot/telegraph_config.json'))
    access_token = config.get('access_token')
    
    # Конвертируем контент
    content_nodes = create_telegraph_content(content, include_title=False)
    
    # Публикуем на Telegra.ph
    url = "https://api.telegra.ph/createPage"
    data = {
        "access_token": access_token,
        "title": title,
        "content": json.dumps(content_nodes),
        "return_content": False
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if not result.get("ok"):
        print(f"❌ Ошибка: {result.get('error', 'Неизвестно')}")
        return None
    
    article_url = result["result"]["url"]
    print(f"✅ Опубликовано: {article_url}")
    
    # Создаём анонс
    escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
    escaped_title = escape_markdown_v2(title)
    escaped_hashtags = hashtags.replace('#', '\\#')
    
    announcement = f"{emoji} [{escaped_title}]({escaped_url})\n\n{escaped_hashtags}"
    
    # Публикуем в Telegram
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
        print(f"✅ Анонс: Message ID {msg_id}")
        return {'url': article_url, 'msg_id': msg_id}
    else:
        print(f"❌ Ошибка Telegram: {tg_result_json.get('description', 'Неизвестно')}")
        return {'url': article_url, 'msg_id': None}

# ============================================================================
# СТАТЬЯ 1
# ============================================================================

ARTICLE_1_TITLE = "ChatGPT, Claude, Gemini: сравниваем топ-3 AI-ассистента 2026"
ARTICLE_1_CONTENT = """Сравниваем трёх лидеров среди универсальных AI-ассистентов. Разбираем возможности, цены и лучшие сценарии использования.

## ChatGPT (OpenAI)

**Модели:**
- GPT-4o — флагшип
- GPT-4o mini — быстрая и дешёвая
- o1 — рассуждения и математика

**Преимущества:**
- 200+ млн пользователей
- Лучшее качество ответов
- Мультимодальность (текст, изображение, звук)
- Магазин GPTs

**Цена:** $20/месяц (Plus)

**Лучше всего подходит для:**
- Универсальных задач
- Написания кода
- Анализа документов

---

## Claude (Anthropic)

**Модели:**
- Claude 3.5 Sonnet — баланс
- Claude 3.5 Opus — максимум
- Claude 3.5 Haiku — быстро

**Преимущества:**
- Контекст 200K токенов
- Безопасные ответы
- Анализ больших документов
- Написание кода

**Цена:** $20/месяц (Pro)

**Лучше всего подходит для:**
- Анализа документов
- Написания кода
- Долгих диалогов

---

## Gemini (Google)

**Модели:**
- Gemini 2.0 Pro — флагшип
- Gemini 2.0 Flash — быстро
- Gemini 2.0 Nano — на устройстве

**Преимущества:**
- Интеграция с Google сервисами
- Мультимодальность
- Поиск информации
- Планирование

**Цена:** $20/месяц (Advanced)

**Лучше всего подходит для:**
- Пользователей Google
- Поиска информации
- Работы с Gmail и Docs

---

## Итоговое сравнение

| Критерий | ChatGPT | Claude | Gemini |
|----------|---------|--------|--------|
| Качество | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Скорость | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Контекст | 128K | 200K | 1M+ |
| Код | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Цена | $20 | $20 | $20 |

## Рекомендации

**Выбирайте ChatGPT, если:**
- Нужен универсальный ассистент
- Важны GPTs и плагины
- Работаете с кодом

**Выбирайте Claude, если:**
- Анализируете большие документы
- Важна безопасность ответов
- Пишете много кода

**Выбирайте Gemini, если:**
- Используете Google сервисы
- Нужен поиск информации
- Важна интеграция с Gmail

---

**Источники:**
- OpenAI Blog
- Anthropic Updates
- Google AI Blog

**Дата:** Март 2026
"""
ARTICLE_1_EMOJI = "🤖"
ARTICLE_1_HASHTAGS = "#ai #chatgpt #claude #gemini #сравнение"

# ============================================================================
# СТАТЬЯ 2
# ============================================================================

ARTICLE_2_TITLE = "Midjourney vs DALL-E 3 vs Stable Diffusion: битва генераторов изображений"
ARTICLE_2_CONTENT = """Сравниваем три популярных генератора изображений на основе ИИ. Какой выбрать для ваших задач?

## Midjourney

**Что решает:**
- Художественные изображения
- Концепт-арт
- Иллюстрации
- Логотипы

**Преимущества:**
- Высокое качество
- Художественный стиль
- Лучшая детализация
- Активное сообщество

**Недостатки:**
- Работа через Discord
- Платный доступ
- Нет локальной установки

**Цена:** $10-120/месяц

**Лучше всего подходит для:**
- Художников
- Дизайнеров
- Концепт-арта

---

## DALL-E 3 (OpenAI)

**Что решает:**
- Генерация по тексту
- Редактирование
- Вариации

**Преимущества:**
- Точное следование промпту
- Интеграция с ChatGPT
- Безопасность контента
- Простота использования

**Недостатки:**
- Только через ChatGPT Plus
- Меньше художественности
- Ограничения контента

**Цена:** $20/месяц (ChatGPT Plus)

**Лучше всего подходит для:**
- Точных запросов
- Быстрых иллюстраций
- Редактирования

---

## Stable Diffusion

**Что решает:**
- Генерация изображений
- Редактирование
- Inpainting/outpainting
- ControlNet

**Преимущества:**
- Открытая модель
- Локальная установка
- Тысячи финетюнов
- Бесплатно

**Недостатки:**
- Требует ресурсов GPU
- Нужно настраивать
- Сложнее в использовании

**Цена:** Бесплатно

**Лучше всего подходит для:**
- Разработчиков
- Локальной установки
- Кастомизации

---

## Итоговое сравнение

| Критерий | Midjourney | DALL-E 3 | Stable Diffusion |
|----------|------------|----------|------------------|
| Качество | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Простота | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Гибкость | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Цена | $10-120 | $20 | Бесплатно |
| Локально | ❌ | ❌ | ✅ |

## Рекомендации

**Выбирайте Midjourney, если:**
- Нужно максимальное качество
- Важна художественность
- Готовы платить $10-120/месяц

**Выбирайте DALL-E 3, если:**
- Нужна простота
- Уже есть ChatGPT Plus
- Важна точность промпта

**Выбирайте Stable Diffusion, если:**
- Нужна локальная установка
- Хотите кастомизировать
- Есть мощный GPU

---

**Источники:**
- Midjourney Documentation
- OpenAI Blog
- Stability AI

**Дата:** Март 2026
"""
ARTICLE_2_EMOJI = "🎨"
ARTICLE_2_HASHTAGS = "#ai #midjourney #dalle #stablediffusion #изображения"

# ============================================================================
# СТАТЬЯ 3
# ============================================================================

ARTICLE_3_TITLE = "GitHub Copilot vs Cursor vs Cline: выбираем AI для разработки кода"
ARTICLE_3_CONTENT = """Сравниваем три популярных инструмента для разработки кода с ИИ.

## GitHub Copilot

**Что решает:**
- Автодополнение кода
- Генерация функций
- Рефакторинг
- Тесты

**Преимущества:**
- Интеграция с IDE
- Поддержка 50+ языков
- Быстрая работа
- Надёжность

**Недостатки:**
- Платный доступ
- Нет чата
- Ограниченный контекст

**Цена:** $10/месяц

**Интеграции:**
- VS Code
- JetBrains
- Neovim
- Visual Studio

**Лучше всего подходит для:**
- Повседневной разработки
- Автодополнения
- Быстрых задач

---

## Cursor

**Что решает:**
- AI-first IDE
- Редактирование через чат
- Поиск по коду
- Автоисправление

**Преимущества:**
- Основан на VS Code
- Локальная обработка
- Интеграция с GitHub
- Умный чат

**Недостатки:**
- Отдельная IDE
- Платный Pro
- Меньше расширений

**Цена:** $20/месяц (Pro)

**Лучше всего подходит для:**
- Новых проектов
- Рефакторинга
- Работы с большой кодобазой

---

## Cline

**Что решает:**
- Автономные задачи
- Работа с терминалом
- Создание файлов
- Отладка

**Преимущества:**
- Open-source
- Локальная работа
- Любая LLM
- Автономность

**Недостатки:**
- Требует настройки
- Меньше интеграций
- Нужно понимать CLI

**Цена:** Бесплатно

**Лучше всего подходит для:**
- Автономных задач
- Локальной разработки
- Экспериментов

---

## Итоговое сравнение

| Критерий | Copilot | Cursor | Cline |
|----------|---------|--------|-------|
| Автодополнение | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Чат | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Автономность | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Цена | $10 | $20 | Бесплатно |
| Простота | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## Рекомендации

**Выбирайте Copilot, если:**
- Нужно автодополнение
- Работаете в VS Code/JetBrains
- Важна скорость

**Выбирайте Cursor, если:**
- Нужен умный чат
- Работаете с большой кодобазой
- Готовы сменить IDE

**Выбирайте Cline, если:**
- Нужна автономность
- Хотите open-source
- Готовы настраивать

---

**Источники:**
- GitHub Blog
- Cursor Documentation
- Cline GitHub

**Дата:** Март 2026
"""
ARTICLE_3_EMOJI = "💻"
ARTICLE_3_HASHTAGS = "#ai #код #copilot #cursor #cline #разработка"

# ============================================================================
# ПУБЛИКАЦИЯ ВСЕХ ТРЁХ СТАТЕЙ
# ============================================================================

print("=" * 60)
print("🚀 ПУБЛИКАЦИЯ 3 СТАТЕЙ")
print("=" * 60)

results = []

# Статья 1
result1 = publish_article(ARTICLE_1_TITLE, ARTICLE_1_CONTENT, ARTICLE_1_EMOJI, ARTICLE_1_HASHTAGS)
if result1:
    results.append(('1', result1))

# Статья 2
result2 = publish_article(ARTICLE_2_TITLE, ARTICLE_2_CONTENT, ARTICLE_2_EMOJI, ARTICLE_2_HASHTAGS)
if result2:
    results.append(('2', result2))

# Статья 3
result3 = publish_article(ARTICLE_3_TITLE, ARTICLE_3_CONTENT, ARTICLE_3_EMOJI, ARTICLE_3_HASHTAGS)
if result3:
    results.append(('3', result3))

# Итог
print("\n" + "=" * 60)
print("📊 ИТОГИ")
print("=" * 60)
print(f"Опубликовано: {len(results)}/3")
for num, res in results:
    print(f"Статья {num}: {res['url']} (Msg ID: {res['msg_id']})")
print("=" * 60)
