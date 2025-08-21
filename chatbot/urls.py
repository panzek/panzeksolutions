from django.urls import path
from . import views, views_upload

urlpatterns = [
    path('api/chat/', views.chat_api, name="chat_api"), # POST API endpoint for frontend fetch
    path('api/upload/', views_upload.upload_document, name="upload_document"), # POST API endpoint for file upload
]