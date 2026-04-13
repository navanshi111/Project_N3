from django.urls import path
from .views import register_view, profile_view, accounts_home
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', accounts_home, name='accounts_home'),
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),]
