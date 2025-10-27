from django.urls import path
from .views import (
    chatbot_view,
    conversation_list_view,
    conversation_detail_view,
    conversation_delete_view,
    conversation_create_view,
)

urlpatterns = [
    path("chat/", chatbot_view, name="chatbot"),
    path("conversations/", conversation_list_view, name="conversation_list"),
    path("conversations/create/", conversation_create_view, name="conversation_create"),
    path("conversations/<int:conversation_id>/", conversation_detail_view, name="conversation_detail"),
    path("conversations/<int:conversation_id>/delete/", conversation_delete_view, name="conversation_delete"),
]
