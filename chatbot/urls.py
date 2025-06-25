from django.urls import path
from . import views

urlpatterns = {
    path('', views.chats, name='chats'),
    path('get_response/', views.chatbot_response, name="chatbot_response")
}