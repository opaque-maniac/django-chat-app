from django.shortcuts import render

from .models import GroupChat

# View for the index page
def chats(request):
    group_chats = GroupChat.objects.filter(participants = request.user)
    context = {'group_chats' : group_chats}
    return render(request, 'chat/chats.html', context)