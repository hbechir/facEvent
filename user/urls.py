from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('home/', views.home, name='home'),
    path('finish_profile/', views.finish_profile, name='finish_profile'),
    path('send_code/', views.send_code, name='send_code'),
    path('verify/', views.verify, name='verify'),
    
    
    # admin routes
    path('get-all-users/', views.get_all_users, name='get_all_users'),
    path('get-all-managers', views.get_all_managers, name='get_all_managers'),

]