import requests
import time

pokemon_name = ["pikachu", "charmander", "bulbasaur", "squirtle", "jigglypuff"]
start = time.time()

for name in pokemon_name:
    url  = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    data = response.json()
    print(f"{data['name'].title()} -> ID: {data['id']}, Types: {[t['type']['name'] for t in data['types']]}")

end = time.time()
print(f"Total time taken: {end - start:.2f} seconds")