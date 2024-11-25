import asyncio
import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker
from urllib.parse import urljoin


def crawl_and_count(url, visited, max_depth, current_depth=0):
    if current_depth >= max_depth or url in visited:
        return
    visited.add(url)
    try:
        r = requests.get(url)

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
                crawl_and_count(absolute_url, visited, max_depth, current_depth + 1)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


async def crawl_and_count_async(url):
    r = requests.get(url)
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


@click.command()
@click.argument("url")
@click.argument("max_links", type=int)
@click.argument("type", type=str)
def gethtml(url, max_links, type):
    visited = set()
    if type == "synchrone":
        crawl_and_count(url, visited, max_links)
    elif type == "asynchrone":
        asyncio.run(crawl_and_count_async(url))


if __name__ == "__main__":
    gethtml()
