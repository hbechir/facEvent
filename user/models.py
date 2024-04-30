from django.db import models
from django.contrib.auth.models import User
import random
from django.utils import timezone


# Create your models here.
class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        # Delete the old code if it exists
        VerificationCode.objects.filter(user=self.user).delete()
        print("generate code")

        # Generate a new random 6-digit code
        self.code = str(random.randint(10000,99999 ))
        self.save()

    def is_valid(self, user):
        # Check if the code is less than 10 minutes old and the user is the same
        return (timezone.now() - self.created_at).total_seconds() < 600 and self.user == user
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15,unique=True)
    verified = models.BooleanField(default=False)
    # faculty = models.CharField(max_length=100, blank=True)
    # department = models.CharField(max_length=100, blank=True)
    # level = models.IntegerField(default=100)
    
    
    def __str__(self):
        return self.user.username