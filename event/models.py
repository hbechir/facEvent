from django.db import models
from club.models import Club, Membership
from django.contrib.auth.models import User





# Create your models here.
class Event(models.Model):
    EVENT_TYPE = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    EVENT_STATUS = [
        ('pending', 'Pending'),   # waiting for approval from admin
        ('rejected', 'Rejected'), # rejected by admin
        ('approved', 'Approved'), # approved by admin
        ('delayed', 'Delayed'),   # delayed by manager
        ('started', 'Started'),
        ('ended', 'Ended'),
        ('canceled', 'Canceled') # cancelled by manager
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to='event_cover', null=True, blank=True)
    organizing_club = models.ForeignKey(Club, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User,null=True, blank=True)
    status = models.CharField(max_length=10,choices=EVENT_STATUS,default='pending')
    starting_date_time = models.DateTimeField()
    ending_date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    max_attendees = models.IntegerField()
    event_type = models.CharField(max_length=10,choices=EVENT_TYPE,default='public')    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def toggle_attend(self, user):
        attendees = self.attendees.all()
        max_attendees = self.max_attendees
        
        # check if user is already in attendee
        if user not in attendees:
            if max_attendees > len(attendees):
                    # check if user is a member of the organizing club
                    if self.event_type == 'private':
                        try:
                            member = Membership.objects.get(user=user, club=self.organizing_club)
                            self.attendees.add(user)
                            self.save()
                            return "You Successfully attended the event.", True
                        except Membership.DoesNotExist:
                            return "You are not a member of the organizing club, You can't attend this event.", False
                    else:
                        self.attendees.add(user)
                        self.save()
                        return "You Successfully attended the event." , True
            else:
                return "max attendees reached,You can't attend this event." , False
        else:
                self.attendees.remove(user)
                self.save()
                return "You Successfully cancelled your attendance." , True
        
        
    def toggle_approval(self):
        if self.status == 'pending':
            self.status = 'approved'
        elif self.status == 'approved':
            self.status = 'rejected'
        elif self.status == 'rejected':
            self.status = 'pending'
        return self.status
    def __str__(self):
        return self.name
    



class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
class Answer(models.Model):
    # question foreign key the field text in Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text