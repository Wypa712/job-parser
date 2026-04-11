import logging
from .config import OPENAI_API_KEY, GROQ_API_KEY, LLM_PROVIDER


def summarize_job(job: dict) -> str:
    if LLM_PROVIDER == "groq" and GROQ_API_KEY:
        return _summarize_with_groq(job)
    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        return _summarize_with_openai(job)
    else:
        return _fallback_summary(job)


def _summarize_with_openai(job: dict) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = (
            "You are a strict job description analyzer. Extract ONLY information from the job text. "
            "Do NOT invent, assume, or speculate. Answer in Ukrainian.\n\n"
            "Respond in plain text (NO Markdown, NO bold, NO *, NO lists). Structure:\n"
            "1. Specialization: [from text]\n"
            "2. Brief description: 2-3 sentences max\n"
            "3. Key skills: comma-separated with details\n"
            "4. Requirements: if present, list key ones\n"
            "5. If information is missing, say 'not specified'\n\n"
            "Max 700 characters. Complete sentences only.\n\n"
            f"Job Title: {job.get('title')}\n"
            f"Company: {job.get('company')}\n"
            f"Location: {job.get('location')}\n"
            f"Description: {job.get('full_description') or job.get('summary')}\n"
            f"Link: {job.get('url')}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
        )
        text = response.choices[0].message.content if response.choices else None
        return text.strip() if text else _fallback_summary(job)
    except Exception as error:
        logging.warning("OpenAI LLM summarization failed: %s", error)
        return _fallback_summary(job)


def _summarize_with_groq(job: dict) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        prompt = (
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
            "- якщо місця мало, скороти обов'язки, але вичеркивай сенс\n"
            "- не використовуй символи * - · для списків\n\n"

            f"Назва: {job.get('title')}\n"
            f"Компанія: {job.get('company')}\n"
            f"Локація: {job.get('location')}\n"
            f"Повний опис: {job.get('full_description') or job.get('summary')}\n"
            f"Посилання: {job.get('url')}"
        )
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
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
