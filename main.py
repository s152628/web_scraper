import requests
import click
from bs4 import BeautifulSoup
import re
from collections import Counter
from spellchecker import SpellChecker


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


if __name__ == "__main__":
    gethtml()
