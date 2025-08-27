import os
import logging
import tempfile 
import boto3
import shutil

from django.http import JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage

logger = logging.getLogger(__name__)
default_storage = S3Boto3Storage()

# Global Rag Vectorstore
RAG_VECTORSTORE = None

def upload_document(request):
    """
    A view for Superuser-only upload endpoint for PDF, TXT, and DOCX.
    Saves to S3 and updates Chroma vectorstore in real-time
    """

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)
    
    allowed_exts = (".pdf", ".txt", ".docx")
    if not any(uploaded_file.name.lower().endswith(ext) for ext in allowed_exts):
        return JsonResponse({"error": f"Only {allowed_exts} are supported."}, status=400)
    
    try:
        # Save to S3
        s3_path = f"uploaded_docs/{uploaded_file.name}"
        file_name = default_storage.save(s3_path, ContentFile(uploaded_file.read()))
        file_url = default_storage.url(file_name)

        # Rebuild vectorstore from files in S3
        global RAG_VECTORSTORE
        RAG_VECTORSTORE = None # force rebuild for debugging
        if RAG_VECTORSTORE is None:
            logger.info("Rebuilding RAG_VECTORSTORE...")
            RAG_VECTORSTORE = build_vectorstore()

        return JsonResponse({
            "Message": f"{uploaded_file.name} uploaded and indexed successfully.",
            "url": file_url
        })

    except Exception as e:
        print("RAG upload error:", repr(e))
        return JsonResponse({"error:", "Upload failed during processing."}, status=500) # 500 server error code
    
def build_vectorstore():
    """
    A view to always pull documents from S3, rebuild embeddings, and persist Chroma to disk
    Logs:
        - Number of raw docs loaded
        - Number of chunks created
        Number of vectors stored in Chroma
    """
    logger.info("Starting build_vectorstore()...")

    # Embed and update Chroma
    CHROMA_DIR = os.path.join(settings.BASE_DIR, "vectorstore", "chroma_db")
    logger.info(f"Using CHROMA_DIR: {CHROMA_DIR}")

    try:

        #Clear conflicting directories
        conflicting_dirs = [
            os.path.join(settings.BASE_DIR, "chroma_db"), 
            os.path.join(settings.BASE_DIR, "vectorstore"),
            os.path.join(settings.BASE_DIR, "vectorstore", "chroma.sqlite3")
        ]

        for dir_path in conflicting_dirs:
            if os.path.exists(dir_path):
                if os.path.isdir(dir_path):
                    shutil.rmtree(dir_path)
                    logger.info(f"Cleared conflicting directory: {dir_path}")
                else:
                    os.remove(dir_path)
                    logger.info(f"Cleared conflicting file: {dir_path}")


        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR)
            logger.info(f"Clear Chroma directory: {CHROMA_DIR}")
            os.makedirs(CHROMA_DIR, exist_ok=True)
            logger.info(f"Created Chroma directory: {CHROMA_DIR}")

    except Exception as e:
        logger.error(f"Error clearing/creating Chroma directory: {e}")
        raise
            
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    documents = []
    s3_prefix = "uploaded_docs/"

    # Use boto3 to list all files recursively
    s3_client = boto3.client('s3')
    bucket_name = default_storage.bucket_name

    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix)
        s3_files = []
        for page in pages:
            for obj in page.get('Contents', []):
                s3_files.append(obj['Key'])
        if not s3_files:
            logger.warning(f"No files found in S3 bucket under {s3_prefix}")
    except ClientError as e:
        logger.error(f"Error listing from S3: {e}")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    
    for file_path in s3_files:
        if not file_path.lower().endswith((".pdf,.txt,.docx")):
            continue

        # Download from Amazon S3 to a temporary file
        with default_storage.open(file_path, "rb") as f:
            suffix = os.path.splitext(file_path)[1].lower()
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as temp:
                temp.write(f.read())
                temp.flush()
                # Choose a loader based on extension
                if suffix == ".pdf":
                    loader = UnstructuredPDFLoader(temp.name)
                elif suffix == ".txt":
                    loader = TextLoader(temp.name)
                elif suffix == ".docx":
                    loader = UnstructuredWordDocumentLoader(temp.name)
                else:
                    logger.warning(f"Skipped unsupported file: {file_path}")
                    continue
                docs = loader.load()
                for doc in docs:
                    logger.info(f"Loaded document {file_path} content )(full): {doc.page_content[:1000]}...")
                documents.extend(docs)
                # logger.info(f"Loaded document {file_path}: {docs[0].page_content[:200]}...")
    
    logger.info(f"Loaded {len(documents)} raw documents from S3")

    if not documents:
        logger.warning("No documents found in S3. Returning empty Chroma DB.")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    # Split into chunks and embed documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE, 
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
        )
    chunks = splitter.split_documents(documents)
    logger.info(f"Split documents into {len(chunks)} chunks (Chunk Size: {settings.RAG_CHUNK_SIZE}, Overlap: {settings.RAG_CHUNK_OVERLAP}).")
    logger.info(f"Created {len(chunks)} chunks")
    if chunks:
        logger.info(f"Sample chunk: {chunks[0].page_content[:200]}...")
        logger.info(f"Split documents into {len(chunks)} chunks (Chunk Size: 1000, Overlap: 200).")
    # for i, chunk in enumerate(chunks[:3]):
    #     logger.debug(f"Sample chunk {i+1}: {chunk.page_content[:200]}")

    # Build and persist Chroma DB
    try:
        vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_DIR
        )
        vectorstore.persist()
    except Exception as e:
        logger.error(f"Error building/persisting Chroma DB: {e}")
        raise 
    vector_count = len(vectorstore.get()['ids'])
    logger.info(f"Chroma DB built successfully with {vector_count} vectors stored.")

    return vectorstore

