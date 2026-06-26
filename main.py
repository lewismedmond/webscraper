import pandas as pd
import requests
from bs4 import BeautifulSoup
from scraper import scrape_pokemon

pokemon = pd.DataFrame(columns=["Name", "Links"])

req = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")

#https://bulbapedia.bulbagarden.net/wiki/Charmander_(Pok%C3%A9mon)

content = req.content
soup = BeautifulSoup(content, "html.parser")
generations = soup.find_all("table", class_="roundy")


names = []
links = []
extra_info = pd.DataFrame(columns = ["Type1", "Type2"]) #, "HP", "ATK", "DEF", "SPATK", "SPDEF", "SPEED", "BST"])

rows = soup.select('table[class*="roundy"] tr[style*="background:#FFF"]')

for row in rows:
  if row.find("td").get("rowspan") != None:
    names.append(row.find_all("td", style = None)[1].text.strip())
    links.append(row.find("a")["href"])
    extra_info.loc[len(extra_info)+1] = scrape_pokemon(links[-1])


#names_with_forms = []

#for generation in generations:
#  names_with_forms.extend([name.text for name in generation.find_all("td", style = None)[1::2]]) 


#pokemon_with_forms = pd.concat([pokemon, pd.DataFrame({"Names_with_forms": names_with_forms})], ignore_index = True)
pokemon = pd.concat([pokemon, pd.DataFrame({"Name":names, "Links":links})], ignore_index = True)


print(pokemon)
print(extra_info)
#print(pokemon_with_forms)


