from django.urls import path
from . import views

urlpatterns = [
    # # normal user ---------------------
    path('',views.get_all_events), # (do not get pending/rejected events)
    path('attend-event', views.attend_event),
    path('ask-question', views.ask_question),
    # # manager --------------------------
    path('request-event', views.request_event),
    path('answer-question', views.answer_question),
    path('cancel-event', views.cancel_event),
    # path('update-event', views.update_event),
    path('event-qa-page', views.event_qa_page),
    path('get-manager-events', views.get_manager_events), # (get all events of clubs managed by manager user)
    path('get-unanswerd-questions', views.get_unanswerd_questions), # (get all unanswerd questions of the events of the clubs managed by manager user) 
    # # admin ----------------------------
    path('toggle-event-status', views.toggle_event_status), # (toggle event status between approved and pending and rejected and )
    path('admin-get-all-events', views.admin_get_all_events), # (get all events)
    
]