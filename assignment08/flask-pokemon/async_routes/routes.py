import asyncio
import random
import time
import httpx
from flask import Blueprint, render_template, current_app

# Create a Blueprint for async routes
async_bp = Blueprint("async", __name__)

# Async function to fetch a single Pokémon
async def get_pokemon(client, url):
    response = await client.get(url)
    print(f"{time.ctime()} - GET {url}")
    return response.json()

# Async function to fetch multiple Pokémon
async def get_pokemons():
    NUMBER_OF_POKEMON = current_app.config.get("NUMBER_OF_POKEMON", 5)
    rand_list = [random.randint(1, 151) for _ in range(NUMBER_OF_POKEMON)]  # Gen 1 Pokémon IDs

    async with httpx.AsyncClient() as client:
        tasks = []
        for number in rand_list:
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(get_pokemon(client, url))
        pokemons = await asyncio.gather(*tasks)  # run all tasks concurrently
    return pokemons

# Async route
@async_bp.route('/')
async def home():
    start_time = time.perf_counter()
    pokemons = await get_pokemons()
    end_time = time.perf_counter()

    print(f"{time.ctime()} - Got {len(pokemons)} Pokémon. Time taken: {end_time - start_time:.2f} seconds")

    return render_template('sync.html',
                           title="Pokémon Async Flask",
                           heading="Random Pokémon (Async)",
                           pokemons=pokemons,
                           end_time=end_time,
                           start_time=start_time)
