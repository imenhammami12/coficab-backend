import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = "https://www.coficab.com"
VISITED = set()
MAX_PAGES = 50  # limite pour ne pas scraper le site entier


def is_internal_link(link: str) -> bool:
    parsed = urlparse(link)
    return parsed.netloc == "" or "coficab.com" in parsed.netloc


def clean_text(soup: BeautifulSoup) -> str:
    # Supprime les éléments non pertinents
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return " ".join(text.split())


def scrape_page(url: str) -> dict | None:
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else url
        content = clean_text(soup)
        links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
        return {"url": url, "title": title, "content": content, "links": links}
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return None


def crawl(start_url: str = BASE_URL, max_pages: int = MAX_PAGES) -> list[dict]:
    to_visit = [start_url]
    pages = []

    while to_visit and len(pages) < max_pages:
        url = to_visit.pop(0)
        url = url.split("#")[0].rstrip("/")

        if url in VISITED or not is_internal_link(url):
            continue

        VISITED.add(url)
        print(f"Scraping: {url}")
        page = scrape_page(url)

        if page and len(page["content"]) > 200:  # ignore les pages quasi vides
            pages.append(page)
            for link in page["links"]:
                clean_link = link.split("#")[0].rstrip("/")
                if clean_link not in VISITED and is_internal_link(clean_link):
                    to_visit.append(clean_link)

        time.sleep(0.5)  # politesse envers le serveur

    return pages


if __name__ == "__main__":
    results = crawl()
    print(f"\n{len(results)} pages scrapées avec succès.")