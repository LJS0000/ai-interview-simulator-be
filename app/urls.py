from django.urls import path, include

urlpatterns = [
    path("api/chat/", include("gpt.urls")),
    path("api/user/", include("user.urls")),
    path("api/accounts/", include("allauth.urls")),
]
