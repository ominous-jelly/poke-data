import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich import padding
import os

# Clear the terminal screen
os.system('clear')

# Creating the rich tables to hold data
main_table = Table(box=box.ROUNDED, title="[bold]Pokedex Data", width=60)
species_table = Table(box=box.ROUNDED, title="[bold]Species Data")
stats_table = Table(box=box.ROUNDED, title="[bold]Base Stats", width=72)
evolution_table = Table(box=box.ROUNDED, title="[bold]Evolutionary Data")

# Creating the dataframe from the CSV file
df = pd.read_csv("../data/pokemon.csv")

# Collecting response
while True:
    try:
        search_input = input("Which Pokemon do you want to see the data for? ")
        os.system('clear')
        # Pulling a row out of the dataframe depending on response
        matching_row = df.loc[df['name'] == search_input.capitalize()]
        break
    except ValueError:
        print("Not a Pokemon. Did you spell it right?")
      
# Turning the dataframe row into a dictionary
result = matching_row.iloc[0].to_dict()

# Gathering data on evolutionary line
evolutionary_matches = df[df['evo_chain'] == result['evo_chain']]
evo_chain = evolutionary_matches['name'].to_list()

# Processing the typing into a single string
typing = ""
if pd.isna(result['type_2']):
    typing = result['type_1']
else:
    typing = result['type_1'] + "/" + result['type_2']

# Processing legendary status into string
classification = ""
if result['is_legendary'] == False:
    classification = "Common"
else:
    classification = "Legendary"

# Creating the tables for output
main_table.add_column("Name", justify='center', width=12)
main_table.add_column("Type", justify='center', width=12)
main_table.add_column("Pokedex #", justify='center', width=12)
main_table.add_column("Generation", justify='center', width=12)
main_table.add_row(result['name'], typing, str(result['#']), result['generation'].upper())

species_table.add_column("Weight", width=15, justify='center')
species_table.add_column("Height", width=15, justify='center')
species_table.add_column("Color", width=15, justify='center')
species_table.add_column("Classification", width=15, justify='center')
species_table.add_row(str(result['weight']) + " kg", str(result['height']) + " cm", result['color'].capitalize(), classification)

stats_table.add_column("HP", justify="center", min_width=12)
stats_table.add_column("Attack", justify="center", min_width=12)
stats_table.add_column("Defense", justify="center", min_width=12)
stats_table.add_column("Sp. Attack", justify="center", min_width=12)
stats_table.add_column("Sp. Defense", justify="center", min_width=12)
stats_table.add_column("Speed", justify="center", min_width=12)
stats_table.add_row(str(result['hp']), str(result['atk']), str(result['def']), str(result['spatk']), str(result['spdef']), str(result['spd']))

for i in range(len(evo_chain)):
    evolution_table.add_column(f"Stage {i + 1}", justify="center")
evolution_table.add_row(*evo_chain)

# Create the console
console = Console()

# Create the pokedex entry panel
dex = Panel.fit(result['pokedex_entry'], title='[bold][italics]Pokedex Entry')
dex = Align.center(dex, vertical='middle')

# Print everything
console.print("\n\n")
console.print(main_table, justify='center')
console.print("\n", dex, "\n")
console.print(species_table, justify='center')
console.print('\n')
console.print(stats_table, justify='center')
console.print('\n')
console.print(evolution_table, justify='center')
console.print('\n\n')