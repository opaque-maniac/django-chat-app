from django.db import models

from accounts.models import CustomUser

# Create your models here.
class Conversation(models.Model):
    participitant = models.ManyToManyField(CustomUser)
    is_group = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'conversation'
        verbose_name_plural = 'conversations'

    def __str__(self):
        return f'Conversation {self.id}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='chat/attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return f'Message {self.id}'
