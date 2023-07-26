from django.urls import path
from .views import ChatbotView

app_name = "gpt"

urlpatterns = [
    path("", ChatbotView.as_view(), name='chatbot'),
]
