from django.db import models
from django.contrib.auth.models import AbstractUser

# extendeds default django built in model that allws us to handle user auth 
class CustomUser(AbstractUser):
    pass
    '''
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField
    '''
    sales_person = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)

 