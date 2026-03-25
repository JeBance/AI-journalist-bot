#!/usr/bin/env python3
"""
AI-journalist Telegram Publisher

Бот для автоматической публикации постов из AI-journalist инфраструктуры.

Использование:
    python3 publisher.py "Текст поста в Markdown V2"

Или через импорт в AI-агенте:
    from publisher import publish
    result = publish("Текст поста")
"""

import sys
import json
import requests
from pathlib import Path

# Путь к файлу конфигурации
CONFIG_FILE = Path(__file__).parent / "config.json"


def load_config():
    """Загрузить конфигурацию из файла."""
    if not CONFIG_FILE.exists():
        print("❌ Файл config.json не найден!")
        print("Создайте файл config.json со следующим содержимым:")
        print(json.dumps({
            "token": "ВАШ_ТОКЕН_БОТА",
            "channel_id": "-100XXXXXXXXXX"
        }, indent=2))
        sys.exit(1)
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def publish(text, parse_mode="MarkdownV2"):
    """
    Опубликовать пост в Telegram канале.
    
    Args:
        text: Текст поста (Markdown V2)
        parse_mode: Режим парсинга (MarkdownV2 или HTML)
    
    Returns:
        dict: Результат от Telegram API
    """
    config = load_config()
    
    token = config["token"]
    channel_id = config["channel_id"]
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": parse_mode
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get("ok"):
            message_id = result["result"]["message_id"]
            print(f"✅ Пост опубликован! Message ID: {message_id}")
            return {
                "success": True,
                "message_id": message_id,
                "response": result
            }
        else:
            error = result.get("description", "Неизвестная ошибка")
            print(f"❌ Ошибка публикации: {error}")
            return {
                "success": False,
                "error": error,
                "response": result
            }
    
    except requests.exceptions.Timeout:
        error = "Превышено время ожидания ответа от Telegram"
        print(f"❌ {error}")
        return {"success": False, "error": error}
    
    except requests.exceptions.ConnectionError:
        error = "Ошибка подключения к Telegram"
        print(f"❌ {error}")
        return {"success": False, "error": error}
    
    except Exception as e:
        error = f"Неожиданная ошибка: {str(e)}"
        print(f"❌ {error}")
        return {"success": False, "error": error}


def test_connection():
    """Проверить соединение с Telegram."""
    config = load_config()
    
    token = config["token"]
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            bot_name = result["result"]["first_name"]
            bot_username = result["result"]["username"]
            print(f"✅ Бот найден: @{bot_username} ({bot_name})")
            return True
        else:
            print("❌ Ошибка проверки токена")
            return False
    
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False


def main():
    """Основная функция."""
    if len(sys.argv) < 2:
        print("AI-journalist Telegram Publisher")
        print("=" * 40)
        print()
        print("Использование:")
        print('  python3 publisher.py "Текст поста"')
        print()
        print("Команды:")
        print("  test — проверить соединение")
        print("  help — показать эту справку")
        print()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "test":
        print("Проверка соединения...")
        test_connection()
    
    elif command == "help":
        print(__doc__)
    
    else:
        # Публикация текста
        text = " ".join(sys.argv[1:])
        publish(text)


if __name__ == "__main__":
    main()
