import aiohttp
from django.contrib.auth.hashers import make_password,check_password
import secrets
from .models import Registrations,Giga_chat_users
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, "index.html")

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        Email=request.POST['Email']
        subject=request.POST['subject']
        message=request.POST['message']

        full_message=f'name:{name},Email:{Email}, subject:{subject} message:{message}'

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,  # From email
                [settings.DEFAULT_FROM_EMAIL],  # To email(s)
                fail_silently=False,
            )

            return render(request, "contact.html" ,{"success":True})
        except Exception as e:
            return render(request, 'contact.html', {'error':str(e)})
    return render(request, 'contact.html')

def about(request):
    admin_dic=[
        {'name':"nika",
        'surname':"kupatadze",
        'age':'18',
        'height':"1.85cm",
        'image':"https://i.pinimg.com/originals/55/c0/15/55c01503b223e297c490055485c872f7.jpg",}
    ]
    return render(request, "about.html", {"admin_dic":admin_dic})


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
    

def info(request):
    if request.method=="POST":
        giga_name = request.POST.get("giga_name")
        giga_surname = request.POST.get("giga_surname")
        giga_age = request.POST.get("giga_age")
        giga_height = request.POST.get("giga_height")

        Giga_chat_users.objects.create(giga_name=giga_name,giga_surname=giga_surname,giga_age=giga_age,giga_height=giga_height)
        return redirect("profile")
    return render(request, "info.html",)

def profile(request):
    session_token=request.session.get('session_token')
    upload=Giga_chat_users.objects.all()
    if session_token:
        user = Registrations.objects.filter(session_token=session_token).values().first()
        user.pop('password')
        user.pop('session_token')
        user.pop('id')
        return render(request, 'profile.html',{"user_data" : user, "upload_giga_chat" : upload})
    else:
        return render(request, 'profile.html',{"user_data" : False, "upload_giga_chat" : upload})
    
    
    

