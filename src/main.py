import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print
from rich.panel import Panel
from rich.align import Align
import os
import create_ascii
from rich.style import Style

# Clear the terminal screen
os.system('clear')

# Creating the dataframe from the CSV file
df = pd.read_csv("../data/pokemon.csv")

# Collecting response from user

while True:
    search_input = input("Which Pokemon do you want to see the data for? ")
    try:
        # Pulling a row out of the dataframe depending on response
        matching_row = df.loc[df['name'] == search_input.capitalize()]
        break
    except IndexError:
        print("Not a Pokemon. Did you spell it right?")
        quit()

# Clearing the screen
os.system('clear')
      
# Turning the dataframe row into a dictionary
result = matching_row.iloc[0].to_dict()

# Gathering data on evolutionary line
evolutionary_matches = df[df['evo_chain'] == result['evo_chain']]
evo_chain = evolutionary_matches['name'].to_list()

# Typing color chart
typing_chart = {
    "Normal": "#A8A77A",
    "Fire": "#EE8130",
    "Water": "#6390F0",
    "Electric": "#F7D02C",
    "Grass": "#7AC74C",
    "Ice": "#96D9D6",
    "Fighting": "#C22E28",
    "Poison": "#A33EA1",
    "Ground": "#E2BF65",
    "Flying": "#A98FF3",
    "Psychic": "#F95587",
    "Bug": "#A6B91A",
    "Rock": "#B6A136",
    "Ghost": "#735797",
    "Dragon": "#6F35FC",
    "Dark": "#705746",
    "Steel": "#B7B7CE",
    "Fairy": "#D685AD"
}

# Processing the typing into a single string
typing = ""
display_style = Style(color=typing_chart[result['type_1']])
secondary_style = Style()

if pd.isna(result['type_2']):
    typing = result['type_1']
else:
    typing = result['type_1'] + "/" + result['type_2']
    secondary_style = Style(color=typing_chart[result['type_2']])

# Processing legendary status into string
classification = ""
if result['is_legendary'] == False:
    classification = "Common"
else:
    classification = "Legendary"

# Creating the tables for output
# Creating the rich tables to hold data
main_table = Table(box=box.ROUNDED, title="[bold]Pokedex Data", width=60, border_style=display_style)
species_table = Table(box=box.ROUNDED, title="[bold]Species Data", border_style=display_style if pd.isna(result['type_2']) else secondary_style)
stats_table = Table(box=box.ROUNDED, title="[bold]Base Stats", width=72, border_style=display_style)
evolution_table = Table(box=box.ROUNDED, title="[bold]Evolutionary Data", min_width=20 , border_style=display_style if pd.isna(result['type_2']) else secondary_style)

main_table.add_column("Name", justify='center', width=12)
main_table.add_column("Type", justify='center', width=12)
main_table.add_column("Pokedex #", justify='center', width=12)
main_table.add_column("Generation", justify='center', width=12)
main_table.add_row(result['name'], f"[{typing_chart[result['type_1']]}]" + typing, str(result['#']), result['generation'].upper())

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
evolution_table.add_row(*evo_chain, style=display_style if pd.isna(result['type_2']) else secondary_style)

# Create the console
console = Console()

# Create the pokedex entry panel
dex = Panel.fit(result['pokedex_entry'], title='[bold][italics]Pokedex Entry', border_style=display_style)
dex = Align.center(dex, vertical='middle')

# Create the image file
create_ascii.main(result['#'])
image_file = open('./ascii_image.txt', 'r').readlines()
image = "".join(image_file)

# Create the image panel
image_panel = Panel(image, title="Image of Pokemon", border_style=display_style)
image_panel = Align.center(image_panel, vertical='middle')

# Print everything
os.system('clear')
console.print(image_panel)
input("Press Enter to Continue...")
os.system('clear')
console.print("\n\n")
console.print(main_table, justify='center')
console.print("\n", dex, "\n")
console.print(species_table, justify='center')
console.print('\n')
console.print(stats_table, justify='center')
console.print('\n')
console.print(evolution_table, justify='center')
console.print('\n\n')
input("Press Enter to Continue...")
os.system('rm -r __pycache__')