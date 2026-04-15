from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import job_list

#urlpatterns = [
    #path('', views.home, name='home'),
    #path('register/', views.register_view, name='register'),
    #path('profile/', views.profile_view, name='profile'),
    #path('login/',auth_views.LoginView.as_view(template_name='careerportal/login.html'),name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    #path("jobs/", job_list, name="jobs"),]

#urlpatterns = [
    #path('', views.home, name='home'),
    #path('register/', views.register_view, name='register'),
    #path('profile/', views.profile_view, name='profile'),
    #path('login/', auth_views.LoginView.as_view(
        #template_name='careerportal/login.html',
        #redirect_authenticated_user=True), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(
       # next_page='home'), name='logout'),
    #path("jobs/", job_list, name="jobs"), ]

# there should only be one urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='careerportal/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'), name='logout'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
]