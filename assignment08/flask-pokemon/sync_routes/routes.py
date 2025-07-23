import time
import random
import requests
from flask import Blueprint, render_template, current_app

# Create a Blueprint for sync routes
sync_bp = Blueprint("sync", __name__)

# Helper function to fetch a single Pokémon JSON by URL
def get_pokemon(url):
    response = requests.get(url)
    print(f"{time.ctime()} - GET {url}")
    return response.json()

# Helper function to fetch multiple Pokémon
def get_pokemons():
    NUMBER_OF_POKEMON = current_app.config.get("NUMBER_OF_POKEMON", 5)  # fallback default = 5
    rand_list = [random.randint(1, 151) for _ in range(NUMBER_OF_POKEMON)]  # Original Gen 1 Pokémon

    pokemon_data = []
    for number in rand_list:
        url = f'https://pokeapi.co/api/v2/pokemon/{number}'
        data = get_pokemon(url)
        pokemon_data.append(data)
    return pokemon_data

# Route: GET /sync/
@sync_bp.route('/')
def home():
    start_time = time.perf_counter()
    pokemons = get_pokemons()
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Got {len(pokemons)} Pokémon. Time taken: {end_time - start_time:.2f} seconds")

    return render_template('sync.html',
                           title="Pokémon Synchronous Flask",
                           heading="Random Pokémon (Sync)",
                           pokemons=pokemons,
                           end_time=end_time,
                           start_time=start_time)
