from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .config import BASE_URL
import requests
from .config import REQUEST_HEADERS


def _safe_text(element):
    return element.get_text(strip=True) if element else ""


def _normalize_job_id(url: str) -> str:
    if not url:
        return ""
    without_query = url.split("?", 1)[0]
    return without_query.rstrip("/")


def parse_jobs(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    job_blocks = soup.select("article")

    if not job_blocks:
        job_blocks = soup.select("a[href*='/stillinger/']")

    jobs = []
    seen_urls = set()

    for block in job_blocks:
        anchor = block.select_one("a[href*='/stillinger/']")
        if anchor is None and block.name == "a" and "/stillinger/" in block.get("href", ""):
            anchor = block

        if anchor is None:
            continue

        relative_url = anchor.get("href", "")
        if not relative_url:
            continue

        url = urljoin(BASE_URL, relative_url)
        if url in seen_urls:
            continue
        seen_urls.add(url)

        title = _safe_text(anchor.select_one("h2") or anchor)
        company = _safe_text(block.select_one("h3") or block.select_one("div[class*='employer']") or block.select_one("span[class*='employer']"))
        location = _safe_text(block.select_one("div[class*='location']") or block.select_one("span[class*='location']") or block.select_one("div[class*='municipality']") or block.select_one("span[class*='municipality']"))
        published = _safe_text(block.select_one("time") or block.select_one("span[class*='published']") or block.select_one("div[class*='published']"))
        summary = _safe_text(block.select_one("p") or block.select_one("div[class*='summary']") or block.select_one("div[class*='description']"))

        if not title:
            title = _safe_text(block.select_one("h2") or block.select_one("h3") or block.select_one("a"))

        if not summary:
            summary = _safe_text(block)
            if len(summary) > 400:
                summary = summary[:400].strip() + "..."

        job_id = _normalize_job_id(url)
        jobs.append({
            "id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "published": published,
            "summary": summary,
            "url": url,
        })

    return jobs


def get_full_job_description(job_url: str) -> str:
    """Завантажує повний опис вакансії з її сторінки."""
    try:
        session = requests.Session()
        session.headers.update(REQUEST_HEADERS)
        response = session.get(job_url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Спробуємо знайти основний опис вакансії
        description = soup.select_one("div[class*='job']") or soup.select_one("div[class*='description']") or soup.select_one("section[class*='description']")
        if description:
            text = description.get_text(strip=True)
            if len(text) > 100:  # Перевіряємо, чи достатньо тексту
                return text
        
        # Альтернативно, візьмемо текст з <main>
        main = soup.select_one("main")
        if main:
            text = main.get_text(strip=True)
            # Видалимо зайві частини, як заголовок, адресу тощо
            # Зазвичай опис починається після "Om jobben" або подібного
            if "Om jobben" in text:
                parts = text.split("Om jobben", 1)
                if len(parts) > 1:
                    return parts[1].strip()
            return text
        
        # Якщо не знайшли, повертаємо весь текст сторінки (але обмежено)
        text = soup.get_text()
        if len(text) > 2000:
            text = text[:2000] + "..."
        return text
    except Exception as e:
        return f"Не вдалося завантажити повний опис: {e}"
