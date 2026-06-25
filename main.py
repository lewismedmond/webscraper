import pandas as pd
import requests
from bs4 import BeautifulSoup

pokemon = pd.DataFrame(columns=["Name", "Names_with_forms"])

req = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")

#https://bulbapedia.bulbagarden.net/wiki/Charmander_(Pok%C3%A9mon)

content = req.content
soup = BeautifulSoup(content, "html.parser")
generations = soup.find_all("table", class_="roundy")

print(len(generations))

names = []
links = []

rows = soup.select('table[class*="roundy"] tr[style*="background:#FFF"]')

for row in rows:

    if row.find("td").get("rowspan") != None:
        names.append(row.find_all("td", style = None)[1].text.strip())


names_with_forms = []

for generation in generations:
    names_with_forms.extend([name.text for name in generation.find_all("td", style = None)[1::2]])


pokemon_with_forms = pd.concat([pokemon, pd.DataFrame({"Names_with_forms": names_with_forms})], ignore_index = True)
pokemon = pd.concat([pokemon, pd.DataFrame({"Name":names})], ignore_index = True)


print(pokemon)
print(pokemon_with_forms)



# -- June 22nd, 2026
# add pokemon to the df one at a time, 
# identify extra forms by checking for a td with a rowspan attribute
# and then probably handle them individually by checking their respective webpages; some forms are competitively distinct(variable) name: Any
