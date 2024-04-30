from django.db import models
from club.models import Club, Member
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    EVENT_TYPE = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    EVENT_STATUS = [
        ('pending', 'Pending'), # waiting for approval from admin
        ('approved', 'Approved'), # approved by admin
        ('started', 'Started'),
        ('delayed', 'Delayed'),
        ('ended', 'Ended'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    organizing_club = models.ForeignKey(Club, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User)
    
    date_time = models.DateTimeField()
    duration_by_hour = models.IntegerField()
    location = models.CharField(max_length=100)
    max_attendees = models.IntegerField()
    type = models.CharField(
        max_length=2,
        choices=EVENT_TYPE,
        default=PUBLIC,
    )    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def attend(self, user): 
        if max_attendees > len(attendees):
            # check if user is already in attendee
            if user not in self.attendees:
                # check if user is a member of the organizing club
                if self.type == 'private':
                    member = Member.objects.get(user=user, club=self.organizing_club)
                    if member:
                        self.attendees.add(user)
                        return True
                    else:
                        return False
                else:
                    self.attendees.add(user)
                    return True
            else:
                self.attendees.remove(user)
                return True
        else:
            return False
    def toggle_approval(self):
        if self.status == 'pending':
            self.status = 'approved'
        else:
            self.status = 'pending'
    
    
    
            
    
    def __str__(self):
        return self.name
    
    