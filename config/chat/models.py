from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class GroupChat(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    participants = models.ManyToManyField(User, related_name='group_chats')
    group_picture = models.ImageField(upload_to="group_pic/", null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    group_chat = models.ForeignKey(GroupChat    , on_delete=models.CASCADE, related_name="group_message", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="chat_pics/", blank=True, null=True)
    attachments = models.FileField(upload_to="chat_files/", blank=True, null=True)
    
    def __str__(self):
        return self.content[:50] + "..."