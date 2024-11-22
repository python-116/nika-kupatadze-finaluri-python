from django.db import models

# Create your models here.
class Registrations(models.Model):
    firstName = models.CharField(max_length=100 ,default='firstname')
    lastName = models.CharField(max_length=100 ,default='lastname')
    userName = models.CharField(max_length=100, unique=True , default='username')
    date = models.DateField()
    email = models.EmailField(unique=True ,default='email')
    password = models.CharField(max_length=255, default='password')
    session_token=models.CharField(max_length=32,default=None,null=True)


    def __st__(self):
        return self.firstname


class Giga_chat_users(models.Model):
    giga_name=models.CharField(max_length=100)
    giga_surname=models.CharField(max_length=100)
    giga_age=models.CharField(max_length=10)
    giga_height=models.CharField(max_length=10)

    def __st__(self):
        return self.giga_name
    
class user_contact(models.Model):
    name=models.CharField(max_length=100)
    Email=models.CharField(max_length=100)
    subject=models.CharField(max_length=200)
    message=models.CharField(max_length=2000)

    def __str__(self):
        return self.name