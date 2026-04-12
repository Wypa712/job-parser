import logging
from .config import GROQ_API_KEY


def summarize_job(job: dict) -> str:
    if GROQ_API_KEY:
        return _summarize_with_groq(job)
    logging.warning("GROQ_API_KEY не налаштовано, використовується fallback.")
    return _fallback_summary(job)


_PROMPT_TEMPLATE = (
    "Ти робиш ТОЧНИЙ АНАЛІЗ вакансії.\n"
    "ЗОЛОТЕ ПРАВИЛО: використовуй ТІЛЬКИ те, що написано в тексті. НЕ вигадуй!\n\n"
    "ФОРМАТ ВІДПОВІДІ (суворо):\n"
    "Простий текст. БЕЗ Markdown, без жирного, без маркерів (*-·), без emoji.\n"
    "Розділи через пусту лінію. Абзаци — короткі.\n\n"
    "СТРУКТУРА:\n"
    "1. Спеціалізація: Яка область роботи?\n"
    "2. Обов'язки: Що саме робити? (2-3 речення)\n"
    "3. Ключові навички: Конкретні вміння/досвід, які хочуть (перелічи через кому, розпиши коротко)\n"
    "4. Вимоги: Освіта, досвід, мови (якщо є в тексті)\n"
    "5. Якщо інформації нема — напиши 'не зазначено'\n\n"
    "ОБМЕЖЕННЯ:\n"
    "- максимум 1800 символів\n"
    "- закінчуй повні речення\n"
    "- не використовуй символи * - · для списків\n\n"
    "Назва: {title}\n"
    "Компанія: {company}\n"
    "Локація: {location}\n"
    "Повний опис: {description}\n"
    "Посилання: {url}"
)


def _build_prompt(job: dict) -> str:
    return _PROMPT_TEMPLATE.format(
        title=job.get("title", ""),
        company=job.get("company", ""),
        location=job.get("location", ""),
        description=job.get("full_description") or job.get("summary", ""),
        url=job.get("url", ""),
    )


def _summarize_with_groq(job: dict) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": _build_prompt(job)}],
            max_tokens=600,
        )
        text = response.choices[0].message.content if response.choices else None
        return text.strip() if text else _fallback_summary(job)
    except Exception as error:
        logging.warning("Groq LLM summarization failed: %s", error)
        return _fallback_summary(job)


def _fallback_summary(job: dict) -> str:
    summary_parts = []
    if job.get("company"):
        summary_parts.append(job["company"])
    if job.get("location"):
        summary_parts.append(job["location"])
    if job.get("summary"):
        summary_parts.append(job["summary"][:180].strip())
    return " | ".join(summary_parts) or "Опис вакансії недоступний."
