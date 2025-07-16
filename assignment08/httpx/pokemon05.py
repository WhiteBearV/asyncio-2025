import asyncio
import httpx

pokemon_names = [
    "pikachu", "bulbasaur", "charmander", "squirtle", "eevee",
    "snorlax", "gengar", "mewtwo", "psyduck", "jigglypuff"
]

async def fetch_pokemon_data(client, name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data['name'].title(),
            "Id": data['id'],
            "Base XP": data['base_experience']
        }
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return None
    

def get_base_xp(pokemon):
    return pokemon["name"]

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch_pokemon_data(client, name) for name in pokemon_names]
        results = await asyncio.gather(*tasks)

    # ลบ None (กรณี error)
    clean_results = [res for res in results if res is not None]

    # เรียงตาม base_experience จากมากไปน้อย
    sorted_pokemon = sorted(clean_results, key=get_base_xp, reverse=True)

    # แสดงผล
    for p in sorted_pokemon:
        print(f"{p["name"]:<12}\t --> ID:{p["Id"]:<5} Base XP:{p["Base XP"]}")

asyncio.run(main())
