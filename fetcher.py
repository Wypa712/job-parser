import requests
from config import BASE_URL, REQUEST_HEADERS


def fetch_job_page() -> str:
    session = requests.Session()
    session.headers.update(REQUEST_HEADERS)
    response = session.get(BASE_URL, timeout=20)
    response.raise_for_status()
    return response.text
