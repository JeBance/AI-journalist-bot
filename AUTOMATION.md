# AI-journalist Автоматизация

## Расписание публикаций

- **00:00 МСК** — 3 статьи
- **02:00 МСК** — 3 статьи
- **06:00 МСК** — 3 статьи

## Файлы

- `/root/git/AI-journalist-bot/publish_3_articles.py` — скрипт публикации
- `/etc/systemd/system/ai-journalist.service` — сервис
- `/etc/systemd/system/ai-journalist-00.timer` — таймер 00:00
- `/etc/systemd/system/ai-journalist-02.timer` — таймер 02:00
- `/etc/systemd/system/ai-journalist-06.timer` — таймер 06:00

## Проверка

```bash
# Проверить таймеры
systemctl list-timers | grep ai-journalist

# Проверить статус
systemctl is-enabled ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer

# Просмотр логов
journalctl -u ai-journalist.service -f

# Просмотр логов за сегодня
journalctl -u ai-journalist.service --since today
```

## Перезапуск после перезагрузки сервера

Таймеры **автоматически** активируются после перезагрузки (enabled).

Если нужно перезапустить вручную:

```bash
systemctl daemon-reload
systemctl restart ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer
```

## Отключение

```bash
# Остановить таймеры
systemctl stop ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer

# Отключить автозагрузку
systemctl disable ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer
```

## Включение

```bash
# Включить таймеры
systemctl start ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer

# Включить автозагрузку
systemctl enable ai-journalist-00.timer ai-journalist-02.timer ai-journalist-06.timer
```

## Тестирование

```bash
# Запустить публикацию вручную
systemctl start ai-journalist.service

# Проверить логи
journalctl -u ai-journalist.service -n 50
```
