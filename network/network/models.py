from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class All_Posts(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    NewPost = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return { 
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    foll = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

class Like(models.Model):
    liker = models.ForeignKey(User, related_name="liking", on_delete=models.CASCADE)
    lik = models.ForeignKey(All_Posts, on_delete=models.CASCADE)