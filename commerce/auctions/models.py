from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class auction_listing(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    class category(models.TextChoices):
        NO_CATEGORY = 'No Category', ('No Category')
        TOYS = 'Toys', ('Toys')
        ARMOR = 'Armor', ('Armor')
        WEAPONS = 'Weapons', ('Weapons')
        BODY_POWERED_DEVICES = 'Body Powered Devices', ('Body Powered Devices')
        TREASURE = 'Treasure', ('Treasure')
    category = models.CharField(
        max_length=100,
        choices=category.choices
    )
    def __str__(self):
        return self.title

class Bid(models.Model):
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name="bids")
    def __str__(self):
        return f"{self.listing}: {self.user} - {self.amount}$"

class Comment(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    comments = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE, related_name="coms")
    def __str__(self):
        return f"{self.listing}: {self.user} - {self.comments}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(auction_listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.listing}: {self.user}"    