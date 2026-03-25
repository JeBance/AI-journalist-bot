#!/usr/bin/env python3
"""
AI-journalist Prompt Updater

Скрипт для обновления промтов AI-агента на основе новых знаний и ошибок.

Использование:
    python3 update_prompts.py --rule "Новое правило"
    python3 update_prompts.py --error "Описание ошибки" --solution "Решение"
    python3 update_prompts.py --show
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Пути к файлам промтов
PROMPTS_DIR = Path(__file__).parent.parent / "AI-journalist" / "01_system_prompts"
LEARNED_FILE = PROMPTS_DIR / "00_learned_prompts.md"
ERROR_LOG_FILE = PROMPTS_DIR / "01_error_log.md"


def get_today_date():
    """Получить сегодняшнюю дату в формате YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def add_learned_rule(rule_text):
    """Добавить новое правило в файл накопленных знаний."""
    date = get_today_date()
    
    if not LEARNED_FILE.exists():
        print(f"❌ Файл {LEARNED_FILE} не найден!")
        return False
    
    # Читаем существующий контент
    with open(LEARNED_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Формируем новую запись
    new_entry = f"""
### {date}: {rule_text}

"""
    
    # Находим раздел "## 🆕 Новые правила"
    marker = "## 🆕 Новые правила"
    if marker in content:
        # Вставляем после заголовка раздела
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n" + new_entry + parts[1]
    else:
        # Если раздел не найден, добавляем в конец
        new_content = content + "\n" + new_entry
    
    # Записываем обновлённый контент
    with open(LEARNED_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Правило добавлено в {LEARNED_FILE}")
    return True


def add_error(error_desc, solution):
    """Добавить ошибку и решение в журнал ошибок."""
    date = get_today_date()
    
    if not ERROR_LOG_FILE.exists():
        print(f"❌ Файл {ERROR_LOG_FILE} не найден!")
        return False
    
    # Читаем существующий контент
    with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Формируем новую запись
    new_entry = f"""
### {date}: {error_desc}

**Ошибка:**
{{описание}}

**Результат:**
{{результат}}

**Решение:**
{solution}

**Правило:** {{краткое правило}}

"""
    
    # Находим раздел "## 📜 История ошибок"
    marker = "## 📜 История ошибок"
    if marker in content:
        # Вставляем после заголовка раздела
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n" + new_entry + parts[1]
    else:
        # Если раздел не найден, добавляем в конец
        new_content = content + "\n" + new_entry
    
    # Записываем обновлённый контент
    with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Ошибка добавлена в {ERROR_LOG_FILE}")
    return True


def show_prompts():
    """Показать содержимое файлов промтов."""
    print("=" * 60)
    print("НАКОПЛЕННЫЕ ЗНАНИЯ (00_learned_prompts.md)")
    print("=" * 60)
    
    if LEARNED_FILE.exists():
        with open(LEARNED_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Файл не найден!")
    
    print("\n" + "=" * 60)
    print("ЖУРНАЛ ОШИБОК (01_error_log.md)")
    print("=" * 60)
    
    if ERROR_LOG_FILE.exists():
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Файл не найден!")


def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(
        description="AI-journalist Prompt Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python3 update_prompts.py --rule "Markdown V2: экранировать #"
  python3 update_prompts.py --error "Не работает публикация" --solution "Проверить токен"
  python3 update_prompts.py --show
        """
    )
    
    parser.add_argument(
        "--rule",
        type=str,
        help="Добавить новое правило в накопленные знания"
    )
    
    parser.add_argument(
        "--error",
        type=str,
        help="Добавить ошибку в журнал (требует --solution)"
    )
    
    parser.add_argument(
        "--solution",
        type=str,
        help="Решение для ошибки"
    )
    
    parser.add_argument(
        "--show",
        action="store_true",
        help="Показать содержимое файлов промтов"
    )
    
    args = parser.parse_args()
    
    if args.show:
        show_prompts()
    
    elif args.rule:
        add_learned_rule(args.rule)
    
    elif args.error:
        if not args.solution:
            print("❌ Для --error требуется --solution")
            sys.exit(1)
        add_error(args.error, args.solution)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
