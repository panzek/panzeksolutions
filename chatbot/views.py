import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.sessions.backends.base import SessionBase

from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from .utils.session_memory import DjangoSessionMessageHistory


def chatbot(request):
    '''
    A view to render the chatbot page
    '''

    return render(request, 'chats.html')


def get_session_history(session):
    """
    A view to create or retrieve a session-based chat history object
    """

    return DjangoSessionMessageHistory(session, key="chat_history")


def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '')

        # response_text = f"Echo: {message}"

        session = request.session
        session_id = session.session_key or session._get_or_create_session_key()

        if not session.get("chat_history"):
            greeting = "Hi, I'm Cece Eleke, an AI assistant. How can I help you today?"
            session["chat_history"] = [{"user": "", "bot": greeting}]

        return JsonResponse({'response': greeting})



