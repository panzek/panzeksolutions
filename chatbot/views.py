import json
import logging
import os
from django.http import JsonResponse
from django.conf import settings

from langchain_core.runnables import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.schema.runnable import RunnableLambda
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .utils.session_memory import DjangoSessionMessageHistory
from .views_upload import RAG_VECTORSTORE, build_vectorstore

logger = logging.getLogger(__name__)

def get_session_history_factory(session):
    """
    A view to create or retrieve a session-based chat history object
    """

    def get_history(session_id):
        return DjangoSessionMessageHistory(session, key=session_id)
    return get_history

def load_vectorstore():
    CHROMA_DIR = os.path.join(settings.BASE_DIR, "vectorstore", "chroma_db")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').strip()
        
        session = request.session
        session_id = session.session_key or session._get_or_create_session_key()

        global RAG_VECTORSTORE
        if RAG_VECTORSTORE is None:
            RAG_VECTORSTORE = load_vectorstore()

        # Debug: Show DB info
        db_info = RAG_VECTORSTORE.get()
        logger.info(f"Number of docs in DB: {len(db_info.get('ids', []))}")
        logger.info(f"RAG_CHUNK_SIZE={settings.RAG_CHUNK_SIZE}, RAG_CHUNK_OVERLAP={settings.RAG_CHUNK_OVERLAP}")

        # Debug: Log retrieved context with scores
        test_docs = RAG_VECTORSTORE.similarity_search_with_score(user_input, k=10)
        logger.info(f"Retrieved {len(test_docs)} chunks for query '{user_input}'") 
        for idx, (doc, score) in enumerate(test_docs): 
            logger.info(f"Chunk {idx+1} (score: {score: .4f}): {doc.page_content[:200]}...")
        if not test_docs:
            logger.warning(f"No chunks retrieved. Possible issues: missing documents, query mismatch, or embedding model limitations")

        # LLM using Gemini
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=1.0,
            api_key=settings.GEMINI_API_KEY
        )

        system_prompt = (
            "You are Cecilia, the official Customer Support Assistant for Panzek Solutions, "
            "a full-stack development company specializing in web development, "
            "eCommerce websites, website maintenance, CMS integration, API integration, "
            "site optimization, server management, web hosting, and chatbot development. "
            "Always respond in a professional, approachable, and solution-oriented tone, "
            "positioning Panzek Solutions as a trusted technology partner. "
            "Provide clear, structured answers, highlight the value of Panzek Solutions' services, "
            "and guide users toward next steps such as sharing requirements, requesting a quote, "
            "or scheduling a consultation. "
            "Only answer questions related to Panzek Solutions' offerings. "
            "Politely decline unrelated requests. "
            "Never provide legal, financial, or personal advice."
            "Keep responses concise (3 sentences max). "
            "Use the following context to answer questions:\n{context}"
        )

        prompt = ChatPromptTemplate(messages=[
            ("system", system_prompt),
            ("placeholder", "{history}"),
            ("human", "{input}"),
        ])

        # Create document chain (stuff type)
        document_chain = create_stuff_documents_chain(llm, prompt)
        # Retrieve from vectorstore
        retriever = RAG_VECTORSTORE.as_retriever(search_kwargs={"k": 10})
        rag_chain = create_retrieval_chain(retriever, document_chain) | RunnableLambda(lambda result: {"output": result["answer"], **result})

        # Set up memory handler via LangChain 
        memory_provider = get_session_history_factory(session)

        runnable = RunnableWithMessageHistory(
            rag_chain,
            memory_provider,
            input_messages_key="input",
            history_messages_key="history",
        )

        try:
            result = runnable.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )

            # Ensure 'output' exists for Langchain callbacks
            response_text = result["output"] 
        
        except Exception as e:
            logger.error("Error from DeepSeek: %s", repr(e))
            response_text = "Sorry, I couldn't process that"

        return JsonResponse({'response': response_text})
    
    return JsonResponse({'error':'Invalid Resquest'}, status=400)



