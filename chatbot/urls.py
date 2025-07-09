from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'), # renders chats.html
    path('chat/', views.chat_api, name="chat_api"), # POST API endpoint for frontend fetch
]

