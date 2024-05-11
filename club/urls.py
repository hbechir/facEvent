from django.urls import path
from . import views

urlpatterns = [
    # normal user ---------------------
    path('',views.get_all_clubs),
    path('request-membership', views.request_membership),
    # admin ----------------------------
    path('add-club/', views.add_club),
    path('delete-club', views.delete_club),
    path('update-club', views.update_club),


    # manager --------------------------
    path('get-club-memberships', views.get_club_memberships),
    path('toggle-membership-state', views.toggle_club_membership_state),

    
]