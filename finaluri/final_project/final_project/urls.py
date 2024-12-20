"""
URL configuration for final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from kuposi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('contact/', views.contact , name='contact'),
    path('about/', views.about , name='about'),
    path('api/', views.APIpage , name='API'),
    path('registration/', views.registration , name='registration'),
    path('login/', views.login , name='login'),
    path('prfile/', views.profile , name='profile'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('info/', views.info , name='info'),


]   