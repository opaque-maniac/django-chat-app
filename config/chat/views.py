from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from . import models
from . import forms
from accounts.models import CustomUser

# View for the landing page
def landing(request):
    if request.user.is_authenticated:
        return redirect('chat:chats')
    return render(request, 'chat/landing.html')

# View for the chats page
@login_required
def chats(request):
    conversations = models.Conversation.objects.all()

    # Retrieve the latest message timestamp for each conversation
    last_message_timestamps = {}
    for conversation in conversations:
        last_message = models.Message.objects.filter(conversation=conversation).order_by('-timestamp').first()
        if last_message:
            last_message_timestamps[conversation.id] = last_message.timestamp.isoformat()
        else:
            last_message_timestamps[conversation.id] = None

    context = { 'conversations': conversations, 'last_message_timestamps': last_message_timestamps }
    return render(request, 'chat/all_chats.html', context)

def check_new_messages(request, conversation_id):
    last_message_timestamp = request.GET.get('last_message_timestamp')
    conversation_messages = models.Message.objects.filter(conversation_id=conversation_id, timestamp__gt=last_message_timestamp).count()

    return JsonResponse({'has_new_messages': conversation_messages > 0})


# View for individual chats
@login_required
def individual_chat(request, conversation_id):
    conversation = models.Conversation.objects.get(id=conversation_id)
    messages = models.Message.objects.filter(conversation=conversation)
    recepient = conversation.participitant.exclude(id=request.user.id).first()
    form = forms.MessageForm()
    context = { 'conversation': conversation, 'messages': messages, 'form': form, 'recepient': recepient }
    return render(request, 'chat/individual_chat.html', context)

# View for retrieving messages
@login_required
def update_messages(request, conversation_id):
    conversation = models.Conversation.objects.get(id=conversation_id)
    messages = models.Message.objects.filter(conversation=conversation)

    html = ""
    for message in messages:
        html += f'<div class="message"><p>{message.content}</p><small>{message.sender.username} - {message.timestamp}</small></div>'

    return JsonResponse({'messages': html})

# View for updating messages
@login_required
def send_message(request, conversation_id):
    if request.method == 'POST':
        conversation = models.Conversation.objects.get(id=conversation_id)
        sender = request.user
        content = request.POST.get('content')

        if content:
            message = models.Message.objects.create(conversation=conversation, sender=sender, content=content)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# View for new chat
@login_required
def new_chat(request, recepient_id):
    recepient = CustomUser.objects.get(id=recepient_id)
    conversation = models.Conversation.objects.create(
        participitant=[request.user, recepient]
    )
    return redirect('chat:individual_chat', conversation.id)

# View for creating a new conversation
@login_required
def new_chat(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        recepients = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
        html = ""
        for recepient in recepients:
            if models.Conversation.objects.filter(participitant__in=[request.user, recepient]).count() == 0:
                html += f'<li><a href="/chat/new/{recepient.id}">{recepient.username}</a></li>'
            else:
                html += f'<li><a href="/chat/chats/{models.Conversation.objects.get(participitant__in=[request.user, recepient]).id}">{recepient.username}</a></li>'
        return JsonResponse({'users': html})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})