from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    field = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    description = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name + ' - ' + self.club.name
    
class Member(models.Model):
    # a user that can be a member of multiple clubs
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username + ' - ' + self.club.name
