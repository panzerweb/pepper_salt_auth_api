from django.urls import path
from .views import RegisterView, LoginView

# URL patterns for authentication endpoints
urlpatterns = [
    # Endpoint for user login
    path("login/", LoginView.as_view()),

    # Endpoint for user registration
    path("register/", RegisterView.as_view()),
]