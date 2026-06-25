import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def scrape_pokemon(pokemon):
  page_req = requests.get("https://bulbapedia.bulbagarden.net/wiki/" + pokemon + "_(Pok%C3%A9mon)")
  page = BeautifulSoup(page_req.content, "html.parser")
  summary = page.select('table[class*="roundy infobox"] tr td[style*="font-size: 85%"]')

  pokemon_types = []
  #print(summary)
  for item in summary:
    if re.search("type", item.find("a")["href"]) and not re.search("Unknown", item.find('b').text.strip()):
      pokemon_types.append(item.find('b').text.strip())
  
  hp_link = page.find("a", title = "HP")
  row = hp_link.find_parent("tr")
  base_hp = row.find_all("div")[1].text.strip()
  print(base_hp)
  return(pokemon_types)

print(scrape_pokemon("Bulbasaur"))