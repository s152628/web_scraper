import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker
from urllib.parse import urljoin


def crawl_and_count(url, counter, visited, max_depth, current_depth=0):
    if current_depth > max_depth or url in visited:
        return
    visited.add(url)
    try:
        r = requests.get(url)
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
                crawl_and_count(
                    absolute_url, counter, visited, max_depth, current_depth + 1
                )

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


@click.command()
@click.argument("url")
def gethtml(url):
    max_links = 2
    counter = Counter()
    visited = set()
    crawl_and_count(url, counter, visited, max_links)


if __name__ == "__main__":
    gethtml()
