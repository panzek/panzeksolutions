from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt;
import json

def get_response(request):
    '''
    A view to return a json formatted data 
    '''

    user_messages = request.GET.get('messages', '')

    responses = {
        "Hello": "Hi, I'm Bessie, an AI assistant to help you find things.",
        "What are your office hours": "Our office is open 9am to 6pm, Monday to Friday",
        "Your services": "We build awesome applications; 'Web Development', 'eCommerce Website', 'Website Maintenance', 'CMS Integration','Site Optimization','Server Management', 'Web Hosting', 'Chatbot'",
        "Bye": "Goodbye, and have a nice day!",
    }

    response = responses.get(user_messages, "I'm sorry, I didn't get that, please rephrase")

    return JsonResponse({'response': response})

@csrf_exempt
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
