import asyncio
import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker
from urllib.parse import urljoin


def fetch_page(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.Timeout:
        print(f"Timeout voor {url}")
    except requests.exceptions.TooManyRedirects:
        print(f"Te veel omleidingen voor {url}")
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het ophalen van {url}: {e}")
    return None


def process_text(text):
    words = re.findall(r"\b\w+\b", text)
    spell = SpellChecker()
    spell_checked_words = [word for word in words if word in spell]
    counted_words = Counter(spell_checked_words)
    return counted_words


def extract_links(soup, url):
    links = soup.find_all("a") + soup.find_all("link")
    absolute_links = []
    for link in links:
        href = link.get("href")
        if href and (
            href.startswith("http://")
            or href.startswith("https://")
            or href.startswith("/")
        ):
            absolute_url = urljoin(url, href)
            absolute_links.append(absolute_url)
    return absolute_links


def crawl_and_count(url, visited, max_links, current_depth=0):
    if current_depth >= max_links or url in visited:
        return
    visited.add(url)

    page_content = fetch_page(url)
    if page_content:
        soup = BeautifulSoup(page_content, "html.parser")
        text = soup.get_text()
        counted_words = process_text(text)
        print(counted_words)

        links = extract_links(soup, url)
        for link in links:
            crawl_and_count(link, visited, max_links, current_depth + 1)


async def crawl_and_count_async(url, visited, max_links, all_counts, current_depth=0):
    if current_depth >= max_links or url in visited:
        return
    visited.add(url)

    page_content = await asyncio.to_thread(fetch_page, url)
    if page_content:
        soup = BeautifulSoup(page_content, "html.parser")
        text = soup.get_text()
        counted_words = process_text(text)
        all_counts.append(counted_words)

        links = extract_links(soup, url)

        tasks = []
        for link in links:
            task = asyncio.create_task(
                crawl_and_count_async(
                    link, visited, max_links, all_counts, current_depth + 1
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks)


@click.command()
@click.argument("url")
@click.argument("max_links", type=int)
@click.argument("type", type=str)
def gethtml(url, max_links, type):
    all_counts = []
    visited = set()

    if type == "synchrone":
        crawl_and_count(url, visited, max_links)
    elif type == "asynchrone":
        asyncio.run(crawl_and_count_async(url, visited, max_links, all_counts))

    for counted_words in all_counts:
        print(counted_words)


if __name__ == "__main__":
    gethtml()
