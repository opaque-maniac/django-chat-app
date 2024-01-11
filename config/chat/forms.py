from django import forms

from . import models

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ['content', 'attachment']
        labels = {
            'content': '',
            'attachment': ''
        }
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'message-input',
                'placeholder': 'Type a message'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Attach a file'
            })
        }