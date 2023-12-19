from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from . import models
from . import forms

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

    return render(request, 'chat/all_chats.html', {'conversations': conversations, 'last_message_timestamps': last_message_timestamps})

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
