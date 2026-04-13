from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Register
    path('register/', views.register_view, name='register'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Login/Logout
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='careerportal/login.html'
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),]