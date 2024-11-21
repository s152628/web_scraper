import requests
import click
from bs4 import BeautifulSoup
import re


@click.command()
@click.argument("url")
def gethtml(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    words = re.findall(r"\b\w+\b", text)

    for word in words:
        print(word)


if __name__ == "__main__":
    gethtml()
