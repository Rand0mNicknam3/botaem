from django.db import models
from user.models import CustomUser


class Follower(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')