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
    
    # Создаём анонс с полным текстом статьи
    escaped_url = article_url.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
    escaped_title = escape_markdown_v2(title)
    
    # Отправляем ПОЛНЫЙ текст статьи в Telegram
    full_text = content.strip()
    
    # Экранируем специальные символы для Markdown V2
    escaped_full_text = escape_markdown_v2(full_text)
    
    # Формируем анонс: заголовок + полный текст + ссылка
    announcement = f"🤖 *{escaped_title}*\n\n{escaped_full_text}\n\n📖 [Читать на Telegra.ph]({escaped_url})\n\n#ai #технологии"
    
    # Публикуем в Telegram
    config = json.load(open('/root/git/AI-journalist-bot/config.json'))
    token = config['token']
    channel_id = config['channel_id']
    
    tg_url = f'https://api.telegram.org/bot{token}/sendMessage'
    
    # Если статья длинная — разбиваем на части
    max_length = 4000  # Telegram лимит 4096, оставляем запас
    chunks = []
    
    if len(announcement) <= max_length:
        chunks = [announcement]
    else:
        # Разбиваем на части по абзацам
        parts = announcement.split('\n\n')
        current_chunk = ""
        
        for part in parts:
            if len(current_chunk) + len(part) + 2 <= max_length:
                current_chunk += part + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = part + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    # Отправляем все части
    msg_id = None
    for i, chunk in enumerate(chunks):
        tg_data = {
            'chat_id': channel_id,
            'text': chunk,
            'parse_mode': 'MarkdownV2'
        }
        
        # Для второй и последующих частей — reply на первую
        if i > 0 and msg_id:
            tg_data['reply_parameters'] = {'message_id': msg_id}
        
        tg_result = requests.post(tg_url, json=tg_data)
        tg_result_json = tg_result.json()
        
        if tg_result_json.get('ok'):
            msg_id = tg_result_json['result']['message_id']
            if i == 0:
                print(f"✅ Анонс опубликован! Message ID {msg_id}")
            else:
                print(f"✅ Часть {i+1} опубликована")
        else:
            print(f"⚠️ Ошибка Telegram: {tg_result_json.get('description', 'Неизвестно')}")
            if i == 0:
                msg_id = None  # Если первая часть не отправлена
    
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
