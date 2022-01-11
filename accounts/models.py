from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
# Create your models here.


GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('None', 'Prefer not to say.'),
]


class User(AbstractUser):
    picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    full_name = models.CharField(max_length=100, help_text='Help people discover your account by using the name you\'re known by: either your full name, nickname, or business name.')
    email = models.EmailField(unique=True)

    # Optional fields
    bio = models.TextField(null=True, blank=True, help_text='Provide your personal information, even if the account is used for a business, a pet or something else. This won\'t be a part of your public profile.')
    # website = models.URLField(null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True)
    # pincode=models.IntegerField(max_length=10,null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    is_private_account = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)



    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)



