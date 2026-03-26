# Инструкция по публикации на GitHub

## AI-journalist-bot

### 1. Добавить remote

```bash
cd /root/git/AI-journalist-bot
git remote add origin https://github.com/JeBance/AI-journalist-bot.git
```

### 2. Переименовать ветку в main

```bash
git branch -M main
```

### 3. Запушить с токеном

```bash
# Замените YOUR_GITHUB_TOKEN на ваш токен
git push -u https://YOUR_GITHUB_TOKEN@github.com/JeBance/AI-journalist-bot.git main
```

### 4. Или через SSH (если настроен)

```bash
git remote set-url origin git@github.com:JeBance/AI-journalist-bot.git
git push -u origin main
```

---

## AI-journalist (основной репозиторий)

Для основного репозитория AI-journalist:

```bash
cd /root/git/AI-journalist
git remote add origin https://github.com/JeBance/AI-journalist.git
git branch -M main
git push -u https://YOUR_GITHUB_TOKEN@github.com/JeBance/AI-journalist.git main
```

---

## Создание токена GitHub

1. Зайдите на https://github.com/settings/tokens
2. Нажмите "Generate new token (classic)"
3. Выберите права: `repo`, `workflow`
4. Скопируйте токен
5. Используйте в команде push

---

**После публикации:**
- AI-journalist: https://github.com/JeBance/AI-journalist
- AI-journalist-bot: https://github.com/JeBance/AI-journalist-bot
