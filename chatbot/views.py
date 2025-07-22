import json
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from langchain_core.runnables import RunnableWithMessageHistory
from langchain_deepseek.chat_models import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate

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
        print("data:", data)
        user_input = data.get('message', '').strip()

        session = request.session
        session_id = session.session_key or session._get_or_create_session_key()

        llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0.6,
            api_key=settings.DEEPSEEK_API_KEY
        )

        # first_name = request.user.first_name if request.user.is_authenticated else "there"

        system_prompt = (
            f"You are a helpful assistant called Cecilia Eleke. "
            "Offer assistance politely. "
            "Use the following context if provided. If you don't know the answer, "
            "just say so. Keep responses concise (3 sentences max). "
        )

        prompt = ChatPromptTemplate([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        chain = prompt | llm

        # Set up memory handler via LangChain 
        runnable = RunnableWithMessageHistory(
            chain,
            lambda session_id: DjangoSessionMessageHistory(request.session, key="chat_history"),
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            response = runnable.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )

            final_response = response.content if hasattr(response, 'content') else str(response)
        
        except Exception as e:
            print("Error from DeepSeek:", repr(e))
            final_response = "Sorry, I couldn't process that"

        return JsonResponse({'response': final_response})
    
    return JsonResponse({'error':'Invalid Resquest'}, status=400)



