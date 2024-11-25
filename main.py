import asyncio
import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker
from urllib.parse import urljoin


def crawl_and_count(url, visited, max_links, current_depth=0):
    if current_depth >= max_links or url in visited:
        return
    visited.add(url)
    try:
        r = requests.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        words = re.findall(r"\b\w+\b", text)
        spell = SpellChecker()
        spell_checked_words = []
        for word in words:
            if word in spell:
                spell_checked_words.append(word)
        counted_words = Counter(spell_checked_words)
        print(counted_words)

        links = soup.find_all("a") + soup.find_all("link")
        for link in links:
            href = link.get("href")
            if href and (
                href.startswith("http://")
                or href.startswith("https://")
                or href.startswith("/")
            ):
                absolute_url = urljoin(url, href)
                crawl_and_count(absolute_url, visited, max_links, current_depth + 1)

    except requests.exceptions.Timeout:
        print(f"Timeout for {url}")
    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects for {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


async def crawl_and_count_async(url, visited, max_links, all_counts, current_depth=0):
    if current_depth >= max_links or url in visited:
        return
    visited.add(url)
    try:
        loop = asyncio.get_event_loop()
        r = await loop.run_in_executor(None, requests.get, url)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()

        words = re.findall(r"\b\w+\b", text)
        spell = SpellChecker()
        spell_checked_words = []
        for word in words:
            if word in spell:
                spell_checked_words.append(word)
        counted_words = Counter(spell_checked_words)
        all_counts.append(counted_words)

        links = soup.find_all("a") + soup.find_all("link")

        tasks = []
        for link in links:
            href = link.get("href")
            if href and (
                href.startswith("http://")
                or href.startswith("https://")
                or href.startswith("/")
            ):
                absolute_url = urljoin(url, href)

                task = asyncio.create_task(
                    crawl_and_count_async(
                        absolute_url, visited, max_links, all_counts, current_depth + 1
                    )
                )
                tasks.append(task)

        await asyncio.gather(*tasks)
    except requests.exceptions.Timeout:
        print(f"Timeout for {url}")
    except requests.exceptions.TooManyRedirects:
        print(f"Too many redirects for {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error for {url}: {e}")


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
