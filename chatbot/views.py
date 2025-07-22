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


def get_session_history_factory(session):
    """
    A view to create or retrieve a session-based chat history object
    """

    def get_history(session_id):
        return DjangoSessionMessageHistory(session, key=session_id)
    return get_history


def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').strip()

        session = request.session
        session_id = session.session_key or session._get_or_create_session_key()

        llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=1.3,
            api_key=settings.DEEPSEEK_API_KEY
        )

        # first_name = request.user.first_name if request.user.is_authenticated else "there"

        system_prompt = (
            "You are a helpful assistant called Cecilia Eleke. "
            "Keep responses concise (3 sentences max). "
        )

        prompt = ChatPromptTemplate(messages=[
            ("system", system_prompt),
            ("placeholder", "{history}"),
            ("human", "{input}"),
        ])

        chain = prompt | llm

        # Set up memory handler via LangChain 
        memory_provider = get_session_history_factory(session)

        runnable = RunnableWithMessageHistory(
            chain,
            memory_provider,
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



