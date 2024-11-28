from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email address')
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    grade = models.CharField(max_length=50, default='Begginer', verbose_name='User grade')

    def __str__(self) -> str:
        return self.username
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }