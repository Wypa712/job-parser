# 🚀 Деплоя на GitHub Actions - Покроковий Гайд

## Крок 1: Підготовка на локальній машині

### 1.1 Перевір, чи Git встановлений
```bash
git --version
```

Якщо помилка, встанови Git з https://git-scm.com/

### 1.2 Налаштуй потрібні ключі в `.env`

Відкрий `.env` файл (або скопіюй з `.env.example`) і заповни:

```
GROQ_API_KEY=xxxxxxxxxxxx          # від https://console.groq.com
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxx    # від @BotFather в Telegram
TELEGRAM_CHAT_ID=xxxxxxxxxxxx      # ID твого чату/каналу
```

**⚠️ Важливо:** OpenAI більше не підтримується - тільки Groq!

Як отримати `TELEGRAM_CHAT_ID`:
- Напиши до своєї особистої чату із ботом `@userinfobot`
- Бот надішле ID (число як `123456789`)

### 1.3 Тестуй локально

```bash
# Активуй virtualenv (на Windows)
venv\Scripts\activate

# Встанови залежності
pip install -r requirements.txt

# Запусти тест
python main.py test
```

Мав бути БЕЗ помилок.

---

## Крок 2: Завантаж на GitHub

### 2.1 Створи репо на GitHub
- Йди на https://github.com/new
- Назва: `job-parser` (або інший)
- **⚠️ Вибери "Public"** (GitHub Actions безплатні для публічних репо)
- Натисни "Create repository"

### 2.2 Завантаж код
```bash
git remote add origin https://github.com/YOUR_USERNAME/job-parser.git
git branch -M main
git push -u origin main
```

---

## Крок 3: Налаштування на GitHub

### 3.1 Додай Secrets
Йди в **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Додай 3 secrets:
- `GROQ_API_KEY` - API ключ від Groq
- `TELEGRAM_BOT_TOKEN` - токен від BotFather
- `TELEGRAM_CHAT_ID` - ID чату для сповіщень

### 3.2 Перевір Actions
- Йди в вкладку **Actions**
- Мав бути workflow "Job Parser - Automated Checks"
- Натисни **Run workflow** для тестового запуску

---

## Крок 4: Моніторинг

### 4.1 Перегляд логів
- **Actions** → Останній запуск
- Клікни на "Run job parser"
- Бачиш логи виконання

### 4.2 Статус
- 🟢 **Зелений** - успішно
- 🔴 **Червоний** - помилка
- 🟡 **Жовтий** - в процесі

---

## ⚙️ Налаштування

### Зміна розкладу
Редагуй `.github/workflows/job-parser.yml`:

```yaml
on:
  schedule:
    - cron: '0 6,18 * * *'  # Зміни 6,18 на потрібні години UTC
```

### Структура проекту
```
demo/
├── main.py              # Головний скрипт
├── src/                 # Python модулі
├── docs/                # Документація
├── data/state.json      # Стан вакансій
└── .github/workflows/   # GitHub Actions
```

---

## 🔧 Вирішення проблем

### "No such file or directory"
- Перевір чи всі файли завантажені на GitHub
- Перевір Secrets

### "API key invalid"
- Перевір GROQ_API_KEY на https://console.groq.com

### "Telegram error"
- Перевір TELEGRAM_BOT_TOKEN та TELEGRAM_CHAT_ID

### Тест локально
```bash
python main.py test
```

---

## 📊 Статистика

- **Запуски:** 2 на день × 30 = 60/місяць
- **Час:** ~10 секунд на запуск
- **Витрати:** 0$ (безплатно для публічних репо)
- **Надійність:** 99.9% uptime

### 2.2 Завантаж код на GitHub

Windows (PowerShell або CMD):
```bash
git init
git add .
git commit -m "Initial job parser setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-parser.git
git push -u origin main
```

Де `YOUR_USERNAME` - твій GitHub ник.

---

## Крок 3: Додай Secret на GitHub

GitHub Actions **потребує** ключи як Secrets, щоб вони не були видимі у коді.

### 3.1 Йди в репо на GitHub
1. **Settings** (вкладинка зверху)
2. **Secrets and variables** (ліва панель) → **Actions**
3. **New repository secret**

### 3.2 Додай 3 Secrets

**3-разово** натисніть **"New repository secret"** та додайте:

| Name | Value |
|------|-------|
| `GROQ_API_KEY` | твій ключ з https://console.groq.com |
| `TELEGRAM_BOT_TOKEN` | ключ від @BotFather |
| `TELEGRAM_CHAT_ID` | ID від @userinfobot |

**Приклад:**
- Name: `GROQ_API_KEY`
- Secret: `gsk_1a2b3c4d5e6f7g8h...`
- Натисніть **"Add secret"**

---

## Крок 4: Запусти GitHub Action вручну

1. Йди на **Actions** вкладинку в твому репо
2. Вибери **"Job Parser - Automated Checks"** (ліва панель)
3. Натисніть **"Run workflow"** → **"Run workflow"**
4. Через 30 секунд має запуститися

---

## Крок 5: Перевір логи

1. **Actions** вкладинка
2. Вибери останній запуск
3. Натисніть на **"check-jobs"** для детальних логів

### Якщо ✅ зелена галочка:
- **Все работает!** Бот буде відправляти повідомлення

### Якщо ❌ червона помилка:
- Переглянь "Run job parser" секцію в логах
- Типові проблеми:
  - ❌ `GROQ_API_KEY not found` → Secret не додахи
  - ❌ `Network error` → Groq API недоступний (рідко)
  - ❌ `Telegram error` → Невірний TELEGRAM_CHAT_ID

---

## Крок 6: Запланован запуски

**GitHub Actions автоматично запускатиме бота:**
- 🕐 **6:00 UTC** (8:00 за часовим поясом Oslo)
- 🕐 **18:00 UTC** (20:00 за часовим поясом Oslo)

Щоденно 2 рази.

Якщо хочеш змінити час, редагуй `.github/workflows/job-parser.yml`:
```yaml
- cron: '0 6,18 * * *'  # Змінь 6 та 18 на потрібні години UTC
```

---

## 🆘 Розв'язання проблем

### ❌ "Repository secret 'XXX' is not found"
**Розв'язок:** Переглянь орфографію Secret. Мав бути точна назва (`GROQ_API_KEY`, не `GROQ_API_Key`).

### ❌ "ModuleNotFoundError: No module named 'groq'"
**Розв'язок:** GitHub Actions не встановив залежності. Перевір `requirements.txt` змарки `groq`.

### ❌ "Telegram error 401 Unauthorized"
**Розв'язок:** TELEGRAM_BOT_TOKEN невірний або закінчився.

### ❌ "Cannot find job in state"
**Розв'язок:** Нормально - означає немає нових вакансій.

---

## ✅ Фінальна перевірка

```
✅ Git залишає встановлено
✅ Репо створено на GitHub (Public)
✅ Код завантажено (git push)
✅ 3 Secrets додано в Settings → Secrets
✅ Workflow існує (.github/workflows/job-parser.yml)
✅ Ручний запуск (Actions → Run workflow) пройшов успішно
```

**Якщо всі ✅ - Ура! Бот запущений! 🎉**

---

## 📊 Моніторинг

- **Кожен запуск:** Actions вкладинка
- **Проблеми:** Actions → job-parser → Найновіший запуск → Логи
- **Статус:** Статус значок збільше списку репо на профілю
