from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import GroupChat

# View for the index page
def index(request):
    return render(request, 'chat/index.html')

# View for all chats page
def chats(request):
    group_chats = GroupChat.objects.filter(participants = request.user)
    context = {'group_chats' : group_chats}
    return render(request, 'chat/chats.html', context)

# View for individual chat page
def individual_chats(request, group_id):
    group = get_object_or_404(GroupChat, id=group_id)
    messages = group.message_set.all()
    context = {'group' : group, 'messages' : messages}
    return render(request, 'chat/individual_chat.html', context)