from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt;
import json

def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        response_text = f"Echo: {message}"

        return JsonResponse({'response': response_text})


def chatbot(request):
    '''
    A view to render the chatbot page
    '''

    return render(request, 'chats.html')
