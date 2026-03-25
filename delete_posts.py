#!/usr/bin/env python3
"""
Удаление постов из Telegram канала.
"""

import sys
import json
import requests

sys.path.insert(0, '/root/git/AI-journalist-bot')

# Загружаем конфиг
config = json.load(open('/root/git/AI-journalist-bot/config.json'))
token = config['token']
channel_id = config['channel_id']

# ID постов для удаления (кроме первого сообщения о запуске бота)
# Message ID 1, 2, 3 - тестовые
# Message ID 4 - первый анонс (заменить)
# Message ID 5, 6, 7, 8 - последующие посты

# Оставляем только Message ID 1 (первое сообщение о запуске)
# Удаляем: 2, 3, 4, 5, 6, 7, 8

posts_to_delete = [2, 3, 4, 5, 6, 7, 8]

url = f'https://api.telegram.org/bot{token}/deleteMessage'

print(f"🗑️ Удаление постов из канала...")
print(f"Канал: {channel_id}")
print(f"Посты для удаления: {posts_to_delete}")
print()

for msg_id in posts_to_delete:
    data = {
        'chat_id': channel_id,
        'message_id': msg_id
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get('ok'):
        print(f"✅ Удалён пост ID: {msg_id}")
    else:
        error = result.get('description', 'Неизвестно')
        print(f"❌ Не удалось удалить пост ID {msg_id}: {error}")

print()
print("Готово!")
