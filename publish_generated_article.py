#!/usr/bin/env python3
"""
Публикация сгенерированной AI статьи.
"""

import sys
import json
sys.path.insert(0, '/root/git/AI-journalist-bot')

from telegraph_publisher import create_telegraph_content
import requests
from datetime import datetime

def escape_markdown_v2(text):
    chars_to_escape = r'_*[]()~`>#+-=|{}.!'
    for char in chars_to_escape:
        text = text.replace(char, f'\\{char}')
    return text

def publish_generated_article():
    """Публикация сгенерированной статьи."""
    
    # Читаем метаданные
    with open('/root/git/AI-journalist-bot/article_metadata.json', 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    title = metadata['title']
    content = metadata['content']
    
    print(f"📝 Публикация: {title}")
    
    # Загружаем конфиги
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
    
    # Извлекаем первые 1-2 предложения для описания (максимум 250 символов)
    description = ""
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('!') and not line.startswith('---'):
            # Берём первые 250 символов и добавляем многоточие если нужно
            description = line[:250]
            if len(line) > 250:
                description += '...'
            break
    
    escaped_description = escape_markdown_v2(description) if description else "AI-статья о технологиях"
    
    announcement = f"🤖 [{escaped_title}]({escaped_url})\n\n{escaped_description}"
    
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
    
    msg_id = None
    if tg_result_json.get('ok'):
        msg_id = tg_result_json['result']['message_id']
        print(f"✅ Анонс: Message ID {msg_id}")
    else:
        print(f"⚠️ Ошибка Telegram: {tg_result_json.get('description', 'Неизвестно')}")
    
    # Запись в историю
    print("\n📝 Запись в историю...")
    
    history_file = '/root/git/AI-journalist/06_history/01_published_posts.md'
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(history_file, 'r', encoding='utf-8') as f:
        history = f.read()
    
    new_entry = f"""### [{today}] {title}

- **Категория:** ai_generated
- **Шаблон:** qwen-code headless
- **Ключевые темы:** AI, автоматическая генерация
- **Telegra.ph URL:** {article_url}
- **Telegram ID:** {msg_id}
- **Статус:** опубликовано (AI-generated)

---

"""
    
    history = history.replace('---\n\n## 📊 Статистика', new_entry + '---\n\n## 📊 Статистика')
    
    with open(history_file, 'w', encoding='utf-8') as f:
        f.write(history)
    
    print("✅ История обновлена!")
    
    return {'url': article_url, 'msg_id': msg_id}

if __name__ == "__main__":
    result = publish_generated_article()
    if result:
        print("\n✅ ПУБЛИКАЦИЯ ЗАВЕРШЕНА!")
    else:
        print("\n❌ ПУБЛИКАЦИЯ НЕ УДАЛАСЬ!")
        sys.exit(1)
