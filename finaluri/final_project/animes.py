import aiohttp
import asyncio

async def API_app(name):
    api = f"https://kitsu.io/api/edge/anime?filter[text]={name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api) as response:
            if response.status == 200:
                data = await response.json()
                if data["data"]: 
                    anime = data["data"][0]["attributes"] 
                    return {
                        "name": anime.get("canonicalTitle"),
                        "score": anime.get("averageRating"),
                        "description": anime.get("synopsis"),
                        "image": anime.get("posterImage", {}).get("original")
                    }
                else:
                    return {"error": "No anime found"}
            else:
                return {"error": f"API error: {response.status}"}

if __name__ == "__main__":
    result = asyncio.run(API_app(input("Enter there : ")))
    if "error" in result:
        print(result["error"])
    else:
        print(result)
