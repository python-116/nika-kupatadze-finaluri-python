import aiohttp
import asyncio
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")


async def anime_API_function(anime_name):
    anime_api = f"https://kitsu.io/api/edge/anime?filter[text]={anime_name}"
    async with aiohttp.ClientSession() as session:
        async with session.get(anime_api) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


async def APIpage(request):
    if request.method == "POST":
        anime_name = request.POST.get("anime_name")
        data = await anime_API_function(anime_name)
        if data and data.get("data"):
            anime_info = data["data"][0]["attributes"]
            name = anime_info.get("canonicalTitle", "Unknown")
            description = anime_info.get("synopsis", "No description available.")
            IMDB = anime_info.get("averageRating", "Not rated")
            image = anime_info.get("posterImage", {}).get("medium", "")

            return render(request, 'APIpage.html', {
                'anime_found': True,
                'name': name,
                'description': description,
                'IMDB': IMDB,
                'image': image,
            })
        else:
            return render(request, 'APIpage.html', {'anime_found': False})
    else:
        return render(request, 'APIpage.html')



