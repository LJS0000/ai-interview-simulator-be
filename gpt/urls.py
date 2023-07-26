from django.urls import path
from .views import ChatView

app_name = "gpt"

urlpatterns = [
    path("", ChatView.as_view(), name='chatbot'),
]
