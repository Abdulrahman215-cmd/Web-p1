from django.contrib import admin
from .models import auction_listing, Bid, Comment, User, Watchlist

# Register your models here.

admin.site.register(auction_listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Watchlist)
