import asyncio
import httpx


url = "https://pokeapi.co/api/v2/ability/?limit=20" 

async def fetch_pokemon_data(client, url):
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        ability_name = data['name'].title()
        Pokemon_list = data['pokemon']
        cont = len(Pokemon_list)
        return (ability_name, cont)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    
async def main():
    async with httpx.AsyncClient() as client:
        # ดึงรายการ ability
        res = await client.get(url)
        res.raise_for_status()
        data = res.json()
        print(data)
        # ดึงแค่ 20 รายการแรก
        ability_urls = [item['url'] for item in data['results'][:20]]

        # สร้าง tasks ไปดึงข้อมูลแบบ concurrent
        tasks = [fetch_pokemon_data(client, url) for url in ability_urls]
        results = await asyncio.gather(*tasks)

    # แสดงผล
    for result in results:
        if result:
            name, count = result
            print(f"{name:<20} → {count} Pokémon")

asyncio.run(main())