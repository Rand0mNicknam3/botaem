from django.db import models
from user.models import CustomUser

class ReferralCode(models.Model):
    # Referral Code
    token = models.CharField(unique=True, max_length=15)
    # Referral code owner
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_code', verbose_name='User')

class ReferralRelationship(models.Model):
    inviter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inviter', verbose_name='Inviter')
    invitee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitee', verbose_name='Invitee')

    def __str__(self):
        return f"{self.inviter} -> {self.invitee}"