import uuid
import os
from django.db import models
from user.models import CustomUser

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, blank=True)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    users_online = models.ManyToManyField(CustomUser, related_name='online_in_groups', blank=True)

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = uuid.uuid4()[:5]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.group_name:
            self.group_name = uuid.uuid4()[:5]
        super().save(*args, **kwargs)
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None
    
    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        elif self.file:
            return f'{self.author.username} : {self.filename}'
    
    def get_image(self):
        profile = self.author.profile
        return profile.image.url
    
    class Meta:
        ordering = ['-created']