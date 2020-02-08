from django.urls import path
from accounts.views import UserRegistrationView, activate
from django.contrib.auth.views import LoginView, LogoutView

# urls
urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
]

