import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def scrape_pokemon(pokemon):
  prefix = "https://bulbapedia.bulbagarden.net/"
  page_req = requests.get(prefix + pokemon) # Finding the right webpage

  page = BeautifulSoup(page_req.content, "html.parser")  # Parsing html
  
  

  

  type_links = page.select('table[class*="roundy infobox"] a[title*="(type)"]') # Selecting hyperlinks from the top right summary that redirect to a type page


  ability_links = page.select('table[class*="roundy infobox"] a[title*="(Ability)"]') # Selecting hyperlinks from the top right summary that redirect to an ability page

 

  pokemon_types = []
  pokemon_abilities = [[],[]]
  
  for item in type_links:
    if item.text.strip() != "Unknown" and not re.search(pokemon.split('_')[0][5::], item.find_parent("td").text):
      pokemon_types.append(item.text.strip())  # Scraping the pokemon's types from the hyperlinks. For some reason there are invisible "Unknown" types


  for item in ability_links:

    if item.text.strip() != "Cacophony":
      if re.search( "Hidden Ability", item.find_parent("td").text):
        pokemon_abilities[1].append(item.text.strip())
      elif not re.search("Mega " + pokemon.split('_')[0][5::], item.find_parent("td").text):
        pokemon_abilities[0].append(item.text.strip())
        # Scraping the pokemon's abilities from the hyperlinks. For some reason there are invisible "Cacophony" abilities

  if(len(pokemon_types) == 1):
    pokemon_types.append("None")
  
  base_stats = []

  hp_link = page.find("a", title = "HP")  # Finding the HP stat hyperlink
  stat_table = hp_link.find_parent("tbody").find_all("th")[4::] # Scraping each stat and the total
  

  for stat in stat_table:
    base_stats.append(stat.find_all("div")[1].text.strip()) # Selecting the actual number
  
  

  return(pokemon_types + pokemon_abilities + base_stats)


print(scrape_pokemon("wiki/Squawkabilly_(Pok%C3%A9mon)"))