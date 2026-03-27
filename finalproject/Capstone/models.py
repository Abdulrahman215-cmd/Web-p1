from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class DirectionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_location} to {self.end_location} ({self.timestamp})"

class Profile(models.Model):
    # CS50 ai suggested that i should make profile model and make a OneToOne field
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Comment(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    comments = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=10, choices=[('Good', 'Good'), ('Bad', 'Bad')])

    def __str__(self):
       return f"{self.user} - {self.comments} - {self.review_type}"