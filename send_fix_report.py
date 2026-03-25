#!/usr/bin/env python3
import sys
sys.path.insert(0, '/root/git/server-bot')
import send_to_telegram

text = """✅ Форматирование исправлено!

🔧 Проблема:
Telegra.ph отображал <b> как текст, а не как форматирование.

💡 Решение:
Telegra.ph требует отдельные узлы для форматирования:

❌ Неправильно:
{"tag": "p", "children": ["<b>Задача:</b> Текст"]}

✅ Правильно:
{"tag": "p", "children": [
  {"tag": "b", "children": ["Задача:"]},
  " Текст"
]}

📰 Новая версия (v7):
https://telegra.ph/10-situacij-gde-II-uzhe-rabotaet-prakticheskoe-rukovodstvo-03-25-7

Анонс: Message ID 14

📁 Обновлён файл:
• telegraph_publisher.py — process_inline_formatting()

🔧 Обработка форматов:
• **текст** → {"tag": "b", "children": ["текст"]}
• _текст_ → {"tag": "i", "children": ["текст"]}
• `код` → {"tag": "code", "children": ["код"]}
• [текст](url) → {"tag": "a", "attrs": {"href": "url"}, "children": ["текст"]}

Теперь жирный текст отображается корректно!"""

send_to_telegram.main(text)
