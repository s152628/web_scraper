import requests
import click


@click.command()
@click.argument("url")
def gethtml(url):
    r = requests.get(url)
    print(r.text)


if __name__ == "__main__":
    gethtml()
