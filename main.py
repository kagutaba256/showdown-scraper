import sys
import json
import csv
import requests
import difflib
from slugify import slugify

if len(sys.argv) != 2:
    print("usage: main.py filename")
    exit(1)

with open(sys.argv[1], "r") as f:
    data = f.readlines()
data = [x.strip() for x in data]

with open('pokemon.csv', 'r') as f:
    reader = csv.reader(f)
    pokedex = dict((rows[1], rows[0]) for rows in reader)

info = {}
info["p1"] = {}
info["p2"] = {}
pokecounter = {}
pokecounter["p1"] = 0
pokecounter["p2"] = 0
turncounter = 0
info['turns'] = []
info['turns'].append([])

useless = [
    "t:",
    "c",
    "upkeep",
    "-message",
    "l",
    "raw"
]


def get_pokedex_entry(name):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if r.status_code == 404:
        return "404 Not Found Sorry"
    return r.json()


for line in data:
    parsed = line[1:].split('|')

    if parsed[0] == 'player':
        info[f"{parsed[1]}"]["name"] = parsed[2]
        info[f"{parsed[1]}"]["elo"] = int(parsed[4])

    elif parsed[0] == 'poke':
        pokecounter[parsed[1]] += 1

        name = slugify(parsed[2].split(',')[0])
        print("Name: " + name)
        name = difflib.get_close_matches(
            name, pokedex.keys(), n=1, cutoff=0.1)[0]
        print("Guess: " + name)
        number = int(pokedex[name])
        info[f"{parsed[1]}"][f"poke{pokecounter[parsed[1]]}"] = {}
        info[f"{parsed[1]}"][f"poke{pokecounter[parsed[1]]}"]['name'] = name
        info[f"{parsed[1]}"][f"poke{pokecounter[parsed[1]]}"]['dex'] = number

    elif parsed[0] == 'win':
        if parsed[1] == info['p1']['name']:
            info['winner'] = "p1"
            info['p1']['won'] = True
            info['p2']['won'] = False
        else:
            info['winner'] = "p2"
            info['p1']['won'] = False
            info['p2']['won'] = True

    elif parsed[0] == 'turn':
        turncounter += 1
        info['turns'].append([])

    elif parsed[0] not in useless:
        info['turns'][turncounter].append(line)

# info['p1']['firstout'] = int(pokedex[slugify(
    # info['turns'][0][-2:][0].split('|')[3].split(',')[0])])
# info['p2']['firstout'] = int(pokedex[slugify(
    # info['turns'][0][-2:][1].split('|')[3].split(',')[0])])

info['turns'].pop(0)

json_str = json.dumps(info, indent=2)
print(json_str)
