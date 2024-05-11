from django.utils import timezone
from .models import Event

def update_events():
    now = timezone.now()
    # get all events that are approved date time is less or equal to now
    events = Event.objects.filter(status='approved', starting_date_time__lte=now)
    for event in events:
            event.status = 'started'
            event.save()
    # get all events that are started and ending date time is less or equal to now
    events = Event.objects.filter(status='started', starting_date_time__lte=now)
    for event in events:
        event.status = 'ended'
        event.save()

    # get all events that are pending and starting date time is less or equal to now
    events = Event.objects.filter(status='pending', starting_date_time__lte=now)
    for event in events:
        event.status = 'rejected'
        event.save()
        
    print('Events Updated')
    
    

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(update_events, 'interval', minutes=15)
