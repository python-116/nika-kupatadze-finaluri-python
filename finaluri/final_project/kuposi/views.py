import aiohttp
from django.contrib.auth.hashers import make_password,check_password
import secrets
from .models import Registrations
from django.shortcuts import render,redirect

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


def registration(request):
    if request.method=="POST":
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        userName = request.POST.get('userName')
        date = request.POST.get('date')
        email = request.POST.get('email')
        password = request.POST.get('password')

        hashed_password=make_password(password)

        Registrations.objects.create(
            firstName = firstName,
            lastName = lastName,
            userName =userName,
            date = date,
            email = email,
            password=hashed_password

        )

        return redirect('index')
        
    return render(request,'registration.html')


def login(request):
    if request.method=="POST":
        userName=request.POST.get('userName')
        password=request.POST.get('password')

        db_password=Registrations.objects.filter(userName=userName).values('password').first()
        if db_password is not None and (check_password(password,db_password['password'])):
            session_token = secrets.token_hex(32)
            request.session['session_token']=session_token
            Registrations.objects.filter(userName=userName).update(session_token=session_token)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error' : 'invalid password or email'})   

    else:
        return render(request, 'login.html')
    
def profile(request):
    session_token=request.session.get('session_token')
    if session_token:
        user = Registrations.objects.filter(session_token=session_token).values().first()
        user.pop('password')
        user.pop('session_token')
        user.pop('id')
        return render(request, 'profile.html',{"user_data" : user})
    else:
        return render(request, 'profile.html',{"user_data" : False})