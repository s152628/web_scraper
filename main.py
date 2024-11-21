import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker
from urllib.parse import urljoin


@click.command()
@click.argument("url")
def gethtml(url):
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
            print(absolute_url)


if __name__ == "__main__":
    gethtml()
