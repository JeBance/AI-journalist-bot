#!/usr/bin/env python3
"""
AI-journalist: qwen-code headless генерация статей.

Запускает qwen-code с промптом для исследования источников и генерации уникальной статьи.
Вдохновлено реализацией QwenAlpha бота.
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Пути
BOT_DIR = Path("/root/git/AI-journalist-bot")
INFRASTRUCTURE_DIR = Path("/root/git/AI-journalist")
HISTORY_FILE = INFRASTRUCTURE_DIR / "06_history" / "01_published_posts.md"
TOPICS_FILE = INFRASTRUCTURE_DIR / "06_history" / "02_topics_covered.md"

def get_last_published_topics():
    """Получить последние опубликованные темы."""
    if not TOPICS_FILE.exists():
        return []
    
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Извлекаем темы из файла
    topics = []
    for line in content.split("\n"):
        if "**Тема:**" in line:
            topic = line.split("**Тема:**")[1].split("|")[0].strip()
            topics.append(topic)
    
    return topics[-10:]  # Последние 10 тем

def generate_article_prompt():
    """Сгенерировать короткий промпт для qwen-code."""
    prompt = """Напиши статью 500 слов для IT-канала.

Тема: новые технологии в разработке ПО.

Структура:
# 🔥 Заголовок статьи

## Введение

2-3 предложения о том, что случилось.

## Детали

Конкретные факты, версии, цитаты.

## Практическая польза

Что это значит для разработчиков.

---

#ai #разработка #технологии

Генерируй полный текст статьи прямо сейчас.
"""
    
    return prompt

def run_qwen_code(prompt):
    """Запустить qwen-code headless через stdin с закрытием stdin."""
    print("🤖 Запуск qwen-code...")
    
    print(f"📝 Запуск qwen с промптом...")
    
    try:
        # qwen читает из stdin, -o text для текстового вывода
        # Важно: закрываем stdin после записи (как в QwenAlpha)
        proc = subprocess.Popen(
            ["qwen", "-o", "text"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "HOME": os.environ.get("HOME", "/root")}
        )
        
        # Записываем промпт и закрываем stdin
        stdout, stderr = proc.communicate(input=prompt, timeout=600)
        
        print(f"qwen завершён (код: {proc.returncode})")
        
        # Сохраняем вывод в файл
        output_file = BOT_DIR / "generated_article.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(stdout)
        
        # Проверяем, создан ли файл
        if output_file.exists() and len(stdout) > 0:
            print(f"✅ Статья сгенерирована! ({len(stdout)} символов)")
            return True
        else:
            print(f"❌ Пустой вывод или ошибка: {stderr[:200] if stderr else 'None'}")
            return False
    
    except subprocess.TimeoutExpired:
        proc.kill()
        print("❌ Превышено время ожидания (10 мин)")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def read_generated_article():
    """Прочитать сгенерированную статью."""
    article_file = BOT_DIR / "generated_article.md"
    
    if not article_file.exists():
        return None, None
    
    with open(article_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Извлекаем заголовок (первая строка после #)
    title = None
    for line in content.split("\n"):
        if line.startswith("# ") and not line.startswith("#!"):
            title = line[2:].strip()
            break
    
    if not title:
        title = f"AI-статья от {datetime.now().strftime('%Y-%m-%d')}"
    
    return title, content

def main():
    """Основная функция."""
    print("=" * 60)
    print("🤖 AI-JOURNALIST: QWEN-CODE HEADLESS ГЕНЕРАЦИЯ")
    print("=" * 60)
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Шаг 1: Генерация промпта
    print("📝 Генерация промпта...")
    prompt = generate_article_prompt()
    
    # Шаг 2: Запуск qwen-code
    success = run_qwen_code(prompt)
    
    if not success:
        print("❌ Не удалось сгенерировать статью")
        return False
    
    # Шаг 3: Чтение статьи
    print("\n📖 Чтение сгенерированной статьи...")
    title, content = read_generated_article()
    
    if not content:
        print("❌ Статья пуста или не найдена")
        return False
    
    print(f"✅ Заголовок: {title}")
    print(f"📊 Объём: {len(content)} символов")
    
    # Шаг 4: Публикация (вызываем publish_article.py)
    print("\n📢 Публикация...")
    
    # Сохраняем метаданные для публикации
    metadata = {
        "title": title,
        "content": content,
        "generated_at": datetime.now().isoformat()
    }
    
    with open(BOT_DIR / "article_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    # Запускаем скрипт публикации
    pub_cmd = [
        "python3",
        str(BOT_DIR / "publish_generated_article.py")
    ]
    
    pub_result = subprocess.run(pub_cmd, capture_output=True, text=True)
    print(pub_result.stdout)
    
    if pub_result.returncode != 0:
        print(f"❌ Ошибка публикации: {pub_result.stderr}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ПУБЛИКАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
