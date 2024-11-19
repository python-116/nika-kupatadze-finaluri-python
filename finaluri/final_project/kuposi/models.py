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
