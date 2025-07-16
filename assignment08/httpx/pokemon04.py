import asyncio
import httpx
import time

pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

async def fetch_pokemon(client, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"{data['name'].title()} -> ID: {data['id']}, Types: {[t['type']['name'] for t in data['types']]}")


        # Not Using Rihght Now
    except httpx.RequestError as e:
        print(f"Request error for {name}: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error for {name}: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon(client, name) for name in pokemon_names]
        await asyncio.gather(*tasks)

start_time = time.time()
asyncio.run(main())
end_time = time.time()

print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")
