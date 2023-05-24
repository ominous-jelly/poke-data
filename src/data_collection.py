import pandas as pd
import requests, json, os, string

API_URL = "https://pokeapi.co/api/v2/"
IMG_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/"

# API calls for data/images

def get_api_data(id, group):
    response = requests.get(API_URL + group + "/" + str(id))
    if response.status_code == 200:
        return response.json()
    else:
        print("Request failed with status code: ", response.status_code)

def scrape_pokemon(json_data):
    return_data = []
    
    # Get name of Pokemon
    return_data.append(json_data["name"].capitalize())
    
    # Get typing of Pokemon
    for i in json_data['types']:
        return_data.append(i['type']['name'].capitalize())
    if len(return_data) == 2:
        return_data.append("")
    
    # Get weight and height of Pokemon
    return_data.append(json_data["weight"])
    return_data.append(json_data['height'])
    
    # Get base stats of Pokemon
    for i in json_data['stats']:
        return_data.append(i["base_stat"])

    return return_data

def scrape_pokemon_species(json_data):
    return_data = []

    # Get legendary status
    return_data.append(json_data['is_legendary'])

    # Get color
    return_data.append(json_data['color']['name'])

    # Get generation
    return_data.append(json_data['generation']['name'].partition('-')[2])

    # Get pokedex entry
    for i in json_data['flavor_text_entries']:
        flavor_text = ""
        if i['language']['name'] == 'en':
            flavor_text = i['flavor_text']
            break
    return_data.append(flavor_text.replace("\n", " ").replace("\u000c", " ").replace("\"", ""))

    # Get what species the Pokemon evolved from
    if json_data['evolves_from_species'] == None:
        return_data.append("base")
    else:
        return_data.append(json_data['evolves_from_species']['name'])
    
    # Get the evolutionary chain ID
    return_data.append(json_data['evolution_chain']['url'][42:-1])
    
    return return_data

def scrape_official_artwork(id):
    if not os.path.exists('../img/'):
        os.makedirs('../img/')
    
    filename = str(id) + ".png"
    r = requests.get(IMG_URL + filename)
    if r.status_code == 200:
        filepath = os.path.join('../img/', filename)
        with open(filepath, 'wb') as file:
            file.write(r.content)
            print(f"Image saved as {filepath}")
    else:
        print("Failed to download image.")

# Placing the data into a dataframe

data = {
    '#': [],
    'name': [],
    'type_1': [],
    'type_2': [],
    'evo_chain': [],
    'evolves_from': [],
    'weight': [],
    'height': [],
    'hp': [],
    'atk': [],
    'def': [],
    'spatk': [],
    'spdef': [],
    'spd': [],
    'color': [],
    'generation': [],
    'is_legendary': [],
    'pokedex_entry': []
}

def add_to_dict(id):
    ds1 = scrape_pokemon(get_api_data(id, 'pokemon'))
    data['#'].append(id)
    data['name'].append(ds1[0])
    data['type_1'].append(ds1[1])
    data['type_2'].append(ds1[2])
    data['weight'].append(ds1[3])
    data['height'].append(ds1[4])
    data['hp'].append(ds1[5])
    data['atk'].append(ds1[6])
    data['def'].append(ds1[7])
    data['spatk'].append(ds1[8])
    data['spdef'].append(ds1[9])
    data['spd'].append(ds1[10])

    ds2 = scrape_pokemon_species(get_api_data(id, 'pokemon-species'))
    data['is_legendary'].append(ds2[0])
    data['color'].append(ds2[1])
    data['generation'].append(ds2[2])
    data['pokedex_entry'].append(ds2[3])
    data['evolves_from'].append(ds2[4])
    data['evo_chain'].append(ds2[5])

    scrape_official_artwork(id)

# Running everything

df = pd.DataFrame()

def create_data_frame(start, stop):
    if not os.path.exists('../data/'):
        os.makedirs('../data/')
    for i in range(start, stop + 1):
        add_to_dict(i)
        print(data['name'][-1] + " added successfully")
        pd.DataFrame(data).to_csv('../data/pokemon.csv', sep=",", index=False)

create_data_frame(1, 905)