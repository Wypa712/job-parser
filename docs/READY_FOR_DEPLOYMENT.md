# 📋 Проект готовий для GitHub Actions

## ✅ Що було підготовлено

### Основні файли проекту:
- ✅ `main.py` - основний скрипт
- ✅ `src/config.py` - конфігурація (тільки Groq)
- ✅ `src/fetcher.py` - завантаження вакансій
- ✅ `src/parser.py` - парсинг HTML + отримання повного опису
- ✅ `src/llm.py` - **Groq LLM аналіз** (OpenAI видалено)
- ✅ `src/storage.py` - зберігання стану в git
- ✅ `src/notifier.py` - Telegram сповіщення
- ✅ `requirements.txt` - залежності (без OpenAI)

### Новостворені файли для деплою:
- ✅ `.github/workflows/job-parser.yml` - GitHub Actions конфіг
- ✅ `.gitignore` - ігнорування конфіденціальних файлів
- ✅ `.env.example` - шаблон для конфігурації
- ✅ `docs/` - вся документація
- ✅ `data/state.json` - стан вакансій (відстежується в git)

---

## 🚀 ШВИДКА ІНСТРУКЦІЯ (5 хвилин)

### 1. Заповни `.env`
Відкрий `.env` та додай 3 значення:
```
GROQ_API_KEY=xxx       # https://console.groq.com
TELEGRAM_BOT_TOKEN=xxx # @BotFather
TELEGRAM_CHAT_ID=xxx   # @userinfobot
```

### 2. Тестуй локально
```bash
python main.py test
```

### 3. Завантаж на GitHub
```bash
git add .
git commit -m "Deploy to GitHub Actions"
git push origin main
```

### 4. Додай Secrets на GitHub
- **Settings** → **Secrets and variables** → **Actions**
- Додай 3 secrets: `GROQ_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

### 5. Запусти тест
- **Actions** → **Job Parser - Automated Checks** → **Run workflow**

✅ **Готово!** Бот буде розсилати вакансії кожен день о 6:00 та 18:00 UTC

---

## 📖 Детальні інструкції

Див. [DEPLOY_GITHUB_ACTIONS.md](DEPLOY_GITHUB_ACTIONS.md) для повного гайду.

---

## ⚙️ Налаштування запусків

Редагуй `.github/workflows/job-parser.yml` щоб змінити час:

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # UTC часи (змінюєш 6 та 18)
```

Час у форматі: `хвилина година * * день_тижня` (UTC)

**Приклади:**
- `0 9,17 * * *` - 9:00 та 17:00 UTC
- `30 6 * * *` - 6:30 UTC кожного дня
- `0 */6 * * *` - кожні 6 годин

---

## 📊 Моніторинг

- **Логи:** Actions вкладинка → Найновіший запуск
- **Проблеми:** Там же, в секції "Run job parser"
- **Помилки:** Будуть показані з red ❌

---

## 🎯 GitHub Actions обмеження (Free Plan)

- ✅ **3000 хвилин/місяц** - достатньо (твої запуски ~10 сек)
- ✅ **Неліміт запусків**
- ✅ **Неліміт репо**

Для твого проекту цього більш ніж достатньо!

---

## 💡 Корисне

### Поточний стан:
- **LLM:** Тільки Groq (швидший і дешевший)
- **Розклад:** 6:00 та 18:00 UTC (8:00 та 20:00 Oslo)
- **Стан:** Зберігається в git між запусками
- **Структура:** Код в `src/`, документація в `docs/`

### Якщо щось не працює:
1. Перевір логи в **Actions** вкладинці
2. Перевір Secrets на GitHub
3. Запусти `python main.py test` локально
- **Actions** → **Job Parser - Automated Checks** → **Run workflow**

✅ **Готово!** Бот буде розсилати вакансії кожен день о 6:00 та 18:00 UTC

---

## 📖 Детальні інструкції

Див. [DEPLOY_GITHUB_ACTIONS.md](DEPLOY_GITHUB_ACTIONS.md) для повного гайду.

---

## ⚙️ Налаштування запусків

Редагуй `.github/workflows/job-parser.yml` щоб змінити час:

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # UTC часи (змінюєш 6 та 18)
```

Час у форматі: `хвилина година * * день_тижня` (UTC)

**Приклади:**
- `0 9,17 * * *` - 9:00 та 17:00 UTC
- `30 6 * * *` - 6:30 UTC кожного дня
- `0 */6 * * *` - кожні 6 годин

---

## 📊 Моніторинг

- **Логи:** Actions вкладинка → Найновіший запуск
- **Проблеми:** Там же, в секції "Run job parser"
- **Помилки:** Будуть показані з red ❌

---

## 🎯 GitHub Actions обмеження (Free Plan)

- ✅ **3000 хвилин/місяц** - достатньо (твої запуски ~10 сек)
- ✅ **Неліміт запусків**
- ✅ **Неліміт репо**

Для твого проекту цього більш ніж достатньо!

---

## 💡 Корисне

- Щоб запустити вручну без очікування: **Actions** → **Run workflow**
- Щоб виключити: Витри `workflow_dispatch` з YAML
- Щоб логи зберігались: Вони автоматично зберігаються 7 днів

---

## 🔗 Посилання

- Groq API: https://console.groq.com
- Telegram BotFather: https://t.me/BotFather
- Telegram userinfobot: https://t.me/userinfobot
- GitHub Actions Docs: https://docs.github.com/en/actions
- Cron формат: https://cron.help

---

**Якщо щось не зрозуміло - перевір DEPLOY_GITHUB_ACTIONS.md!** 📖
