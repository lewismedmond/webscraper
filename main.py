import pandas as pd
import requests
from bs4 import BeautifulSoup

pokemon = pd.DataFrame(columns=["Name"])

req = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")

content = req.content
soup = BeautifulSoup(content, "html.parser")
generations = soup.find_all("table", class_="roundy")

print(len(generations))

names = []
links = []

for generation in generations:
    names.extend([item.text for item in generation.find_all("td", style = None)[1::2]])  # This will print the names of the Pokémon in the first generation
    links.extend([item.find("a")["href"] for item in generation.find_all("td", style = None)[1::2]])  # This will print the links of the Pokémon in the first generation


for name, link in zip(names, links):
    pokemon = pd.concat([pokemon, pd.DataFrame({"Name": [name]})], ignore_index=True)

print(pokemon)


# -- June 22nd, 2026
# add pokemon to the df one at a time, 
# identify extra forms by checking for a td with a rowspan attribute
# and then probably handle them individually by checking their respective webpages; some forms are competitively distinct