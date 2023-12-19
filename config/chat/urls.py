from django.urls import path
from . import views

app_name = 'chat'

# Urls for the chat app
urlpatterns = [
    path('', views.landing, name='index'),
    path('chats/', views.chats, name='chats'),
    path('chats/<int:conversation_id>/', views.individual_chat, name='individual_chat'),
    path('chats/<int:conversation_id>/update_messages/', views.update_messages, name='update_messages'),
    path('chats/<int:conversation_id>/send_message/', views.send_message, name='send_message'),
    path('chats/<int:conversation_id>/check_new_messages/', views.check_new_messages, name='check_new_messages'),
]