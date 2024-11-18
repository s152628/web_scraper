from bs4 import BeautifulSoup

print("Geef een path naar een html bestand")
input_path = input("> ")

with open(input_path, "r") as file:
    content = file.read()

soup = BeautifulSoup(content, "html.parser")

print(soup.prettify())
