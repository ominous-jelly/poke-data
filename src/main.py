import pandas as pd


df = pd.read_csv("data/pokemon.csv")
search_input = input("Which Pokemon do you want to see the data for? ")
matching_row = df.loc[df['name'] == search_input.capitalize()]

result = matching_row.iloc[0].to_dict()

def print_results(pokemon):
    print("Number " + str(result['#']) + ": " + result['name'])
    if pd.isna(result['type_2']) == True:
        print("Typing: " + result['type_1'])
    else:
        print("Typing: " + result['type_1'] + "/" + result['type_2'])
print_results(result)