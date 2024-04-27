from django.urls import path
from . import views

urlpatterns = [
    path('/register/', views.register_user, name='register'),
    path('/home/', views.home, name='home'),
    path('/finish_profile/', views.finish_profile, name='finish_profile'),

]