import requests

url  = "https://pokeapi.co/api/v2/pokemon/pikachu"
response = requests.get(url)

data = response.json()

print(f"Name: {data['name']}")
print(f"Height: {data['height']}")
print(f"Weight: {data['weight']}")
print(f"Types:", [type_info['type']['name'] for type_info in data['types']])