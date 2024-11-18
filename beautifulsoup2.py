from bs4 import BeautifulSoup

print("Geef een path naar een html bestand")
input_path = input("> ")

with open(input_path, "r") as file:
    content = file.read()

soup = BeautifulSoup(content, "html.parser")

jpgs = soup.find_all("img")
for jpg in jpgs:
    if jpg["src"].endswith(".jpg"):
        print(jpg["src"])
