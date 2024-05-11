from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField()
    logo = models.ImageField(upload_to='club_logo', null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    field = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    def __str__(self):
        return self.name


    
class Membership(models.Model):
    MEMBERSHIP_STATE = {
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('REJECTED', 'Rejected'),
        ('REMOVED', 'Removed'),
    }
    
    
    # a user that can be a member of multiple clubs
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.CharField(max_length=100,default='MEMBER')
    joined_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=100, choices=MEMBERSHIP_STATE, default='PENDING')
                

    def toggle_club_membership_state(self):
        if self.state == 'PENDING':
            self.state = 'ACTIVE'
        elif self.state == 'ACTIVE':
            self.state = 'REMOVED'
        elif self.state == 'REMOVED':
            self.state = 'PENDING'
        self.save()
        return self.state

    def __str__(self):
        return self.user.username + ' - ' + self.club.name
