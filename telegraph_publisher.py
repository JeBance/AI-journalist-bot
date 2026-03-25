#!/usr/bin/env python3
"""
Telegra.ph Publisher

Публикация статей на Telegra.ph и создание анонса для Telegram канала.

Использование:
    python3 telegraph_publisher.py "Заголовок" "Содержание статьи" "Автор"
    
Или через импорт:
    from telegraph_publisher import publish_article
    result = publish_article("Заголовок", "Содержание", "Автор")
"""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# Путь к файлу конфигурации
CONFIG_FILE = Path(__file__).parent / "telegraph_config.json"


def load_config():
    """Загрузить конфигурацию Telegra.ph."""
    if not CONFIG_FILE.exists():
        print("❌ Файл telegraph_config.json не найден!")
        print("Создайте файл со следующим содержимым:")
        print(json.dumps({
            "short_name": "AI Journalist",
            "author_name": "AI Journalist",
            "author_url": "https://t.me/JeBanceOnline"
        }, indent=2))
        sys.exit(1)
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def create_telegraph_content(markdown_text, include_title=False):
    """
    Конвертировать Markdown в формат Telegra.ph (JSON).
    
    Telegra.ph использует Array of Node.
    Списки должны быть в ul/ol с li элементами.
    
    Args:
        markdown_text: Текст в формате Markdown
        include_title: Если False — пропускаем первый заголовок И первый параграф (Telegra.ph добавляет заголовок автоматически)
    """
    content = []
    lines = markdown_text.split('\n')
    
    current_paragraph = []
    current_list = []
    in_list = False
    skip_first_h3 = not include_title
    skip_first_paragraph = not include_title  # Пропускаем первый параграф (это описание под заголовком)
    
    for line in lines:
        line = line.strip()
        
        if not line:
            # Пустая строка - закрываем параграф и список
            if current_paragraph:
                if not skip_first_paragraph:
                    content.append({
                        "tag": "p",
                        "children": [" ".join(current_paragraph)]
                    })
                else:
                    skip_first_paragraph = False
                current_paragraph = []
            
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            continue
        
        # Заголовки
        if line.startswith('### '):
            # Пропускаем первый заголовок (это заголовок статьи)
            if skip_first_h3:
                skip_first_h3 = False
                continue
            
            # Закрываем предыдущие элементы
            if current_paragraph:
                content.append({
                    "tag": "p",
                    "children": [" ".join(current_paragraph)]
                })
                current_paragraph = []
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            
            content.append({
                "tag": "h3",
                "children": [line[4:]]
            })
        elif line.startswith('## '):
            if current_paragraph:
                content.append({
                    "tag": "p",
                    "children": [" ".join(current_paragraph)]
                })
                current_paragraph = []
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            
            content.append({
                "tag": "h3",
                "children": [line[3:]]
            })
        elif line.startswith('# '):
            if current_paragraph:
                content.append({
                    "tag": "p",
                    "children": [" ".join(current_paragraph)]
                })
                current_paragraph = []
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            
            content.append({
                "tag": "h3",
                "children": [line[2:]]
            })
        # Списки (· или -)
        elif line.startswith('· ') or line.startswith('- '):
            in_list = True
            current_list.append({
                "tag": "li",
                "children": [line[2:]]
            })
        # Код
        elif line.startswith('```'):
            continue
        # Цитаты
        elif line.startswith('> '):
            if current_paragraph:
                content.append({
                    "tag": "p",
                    "children": [" ".join(current_paragraph)]
                })
                current_paragraph = []
            if in_list and current_list:
                content.append({
                    "tag": "ul",
                    "children": current_list
                })
                current_list = []
                in_list = False
            
            content.append({
                "tag": "blockquote",
                "children": [line[2:]]
            })
        # Обычный текст
        else:
            # Обработка inline форматирования
            # Telegra.ph требует отдельные узлы для форматирования, не HTML!
            
            import re
            
            def process_inline_formatting(text):
                """
                Разбить текст на узлы с форматированием.
                Возвращает список строк и узлов.
                """
                parts = []
                remaining = text
                
                # Обрабатываем **жирный**
                if '**' in remaining:
                    new_parts = []
                    last_end = 0
                    for match in re.finditer(r'\*\*(.+?)\*\*', remaining):
                        if match.start() > last_end:
                            new_parts.append(remaining[last_end:match.start()])
                        new_parts.append({"tag": "b", "children": [match.group(1)]})
                        last_end = match.end()
                    if last_end < len(remaining):
                        new_parts.append(remaining[last_end:])
                    remaining = new_parts if new_parts else [remaining]
                else:
                    remaining = [remaining]
                
                # Обрабатываем каждый элемент на курсив, код, ссылки
                final_parts = []
                for part in remaining:
                    if isinstance(part, dict):
                        final_parts.append(part)
                    else:
                        # _курсив_
                        if '_' in part:
                            new_parts = []
                            last_end = 0
                            for match in re.finditer(r'_(.+?)_', part):
                                if match.start() > last_end:
                                    new_parts.append(part[last_end:match.start()])
                                new_parts.append({"tag": "i", "children": [match.group(1)]})
                                last_end = match.end()
                            if last_end < len(part):
                                new_parts.append(part[last_end:])
                            final_parts.extend(new_parts if new_parts else [part])
                        else:
                            final_parts.append(part)
                
                # `код`
                processed = []
                for part in final_parts:
                    if isinstance(part, dict):
                        processed.append(part)
                    else:
                        if '`' in part:
                            new_parts = []
                            last_end = 0
                            for match in re.finditer(r'`(.+?)`', part):
                                if match.start() > last_end:
                                    new_parts.append(part[last_end:match.start()])
                                new_parts.append({"tag": "code", "children": [match.group(1)]})
                                last_end = match.end()
                            if last_end < len(part):
                                new_parts.append(part[last_end:])
                            processed.extend(new_parts if new_parts else [part])
                        else:
                            processed.append(part)
                
                # [ссылка](url)
                final = []
                for part in processed:
                    if isinstance(part, dict):
                        final.append(part)
                    else:
                        if '[' in part and '](' in part:
                            new_parts = []
                            last_end = 0
                            for match in re.finditer(r'\[(.+?)\]\((.+?)\)', part):
                                if match.start() > last_end:
                                    new_parts.append(part[last_end:match.start()])
                                new_parts.append({
                                    "tag": "a",
                                    "attrs": {"href": match.group(2)},
                                    "children": [match.group(1)]
                                })
                                last_end = match.end()
                            if last_end < len(part):
                                new_parts.append(part[last_end:])
                            final.extend(new_parts if new_parts else [part])
                        else:
                            final.append(part)
                
                return final
            
            # Обрабатываем строку
            parts = process_inline_formatting(line)
            
            # Проверяем, есть ли вложенные узлы
            has_nodes = any(isinstance(p, dict) for p in parts)
            
            if has_nodes:
                # Создаём параграф с children
                content.append({
                    "tag": "p",
                    "children": parts
                })
            else:
                # Простой текст
                current_paragraph.append("".join(parts))
    
    # Добавляем оставшиеся элементы
    if current_paragraph:
        if not skip_first_paragraph:
            content.append({
                "tag": "p",
                "children": [" ".join(current_paragraph)]
            })
    
    if in_list and current_list:
        content.append({
            "tag": "ul",
            "children": current_list
        })
    
    return content


def publish_article(title, content, author=None, return_content=False):
    """
    Опубликовать статью на Telegra.ph.
    
    Args:
        title: Заголовок статьи
        content: Содержимое (Markdown или список JSON элементов)
        author: Автор статьи
        return_content: Вернуть ли полный контент для отладки
    
    Returns:
        dict: Результат с URL статьи
    """
    config = load_config()
    
    # Получаем токен из конфига
    access_token = config.get("access_token")
    
    if not access_token:
        print("❌ Access Token не найден в конфигурации!")
        print("Запустите: python3 get_telegraph_token.py")
        return {"success": False, "error": "No access token"}
    
    # Конвертируем Markdown в JSON если нужно
    if isinstance(content, str):
        content_nodes = create_telegraph_content(content)
    else:
        content_nodes = content
    
    # URL API Telegra.ph
    url = "https://api.telegra.ph/createPage"
    
    data = {
        "access_token": access_token,
        "title": title,
        "content": json.dumps(content_nodes),
        "return_content": return_content
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get("ok"):
            article_url = result["result"]["url"]
            article_id = result["result"]["path"]
            print(f"✅ Статья опубликована!")
            print(f"📰 URL: {article_url}")
            print(f"🆔 ID: {article_id}")
            
            return {
                "success": True,
                "url": article_url,
                "id": article_id,
                "title": title,
                "response": result
            }
        else:
            error = result.get("error", "Неизвестная ошибка")
            print(f"❌ Ошибка публикации: {error}")
            return {
                "success": False,
                "error": error,
                "response": result
            }
    
    except requests.exceptions.Timeout:
        error = "Превышено время ожидания"
        print(f"❌ {error}")
        return {"success": False, "error": error}
    
    except Exception as e:
        error = f"Ошибка: {str(e)}"
        print(f"❌ {error}")
        return {"success": False, "error": error}


def create_announcement_post(article_url, title, description=""):
    """
    Создать пост-анонс для Telegram канала.
    
    Args:
        article_url: URL статьи на Telegra.ph
        title: Заголовок статьи
        description: Краткое описание
    
    Returns:
        str: Текст поста для Telegram
    """
    post = f"""📖 *Новая статья на Telegra.ph*

*{title}*

{description}

[Читать полностью →]({article_url})

\#статья \#telegraph"""
    
    return post


def publish_with_announcement(title, content, description="", telegram_publish=False):
    """
    Опубликовать статью на Telegra.ph и создать анонс.
    
    Args:
        title: Заголовок статьи
        content: Содержимое статьи (Markdown)
        description: Краткое описание для анонса
        telegram_publish: Опубликовать ли анонс в Telegram
    
    Returns:
        dict: Результат публикации
    """
    print("📝 Публикация статьи на Telegra.ph...")
    article_result = publish_article(title, content)
    
    if not article_result["success"]:
        return article_result
    
    print("\n📢 Создание анонса...")
    announcement = create_announcement_post(
        article_result["url"],
        title,
        description
    )
    
    print("Анонс:")
    print("-" * 40)
    print(announcement)
    print("-" * 40)
    
    if telegram_publish:
        print("\n🚀 Публикация анонса в Telegram...")
        from publisher import publish
        telegram_result = publish(announcement)
        article_result["telegram"] = telegram_result
    
    return article_result


def main():
    """Основная функция."""
    if len(sys.argv) < 2:
        print("Telegra.ph Publisher")
        print("=" * 40)
        print()
        print("Использование:")
        print('  python3 telegraph_publisher.py "Заголовок" "Содержание" "Автор"')
        print()
        print("Команды:")
        print("  help — показать эту справку")
        print()
        sys.exit(0)
    
    if sys.argv[1] == "help":
        print(__doc__)
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print("❌ Недостаточно аргументов!")
        print("Используйте: python3 telegraph_publisher.py \"Заголовок\" \"Содержание\"")
        sys.exit(1)
    
    title = sys.argv[1]
    content = sys.argv[2]
    author = sys.argv[3] if len(sys.argv) > 3 else None
    
    publish_article(title, content, author)


if __name__ == "__main__":
    main()
