from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AuctionListingForm, BidForm, CommentForm
from .models import User, auction_listing, Bid, Watchlist


def index(request):
    listings = auction_listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.seller = request.user
            auction_listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
        })

def save_new_bid(bid_form, user, listing):
                    new_bid_an = bid_form.save(commit=False)
                    new_bid_an.user = user
                    new_bid_an.listing = listing
                    new_bid_an.save()

@login_required(login_url="login")
def list_item(request, title):
    try:
        listed = auction_listing.objects.get(title=title)
    except auction_listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    new_bid = None
    highest_bid = None
    bids = listed.bids.all()
    if request.method == "POST":
        if "close_auction" in request.POST:
            if highest_bid:
                listed.winner = highest_bid.user
            listed.is_active = False
            listed.save()
            return HttpResponseRedirect(reverse("index"))
        elif "submit_bid" in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                new_bid = bid_form.cleaned_data['amount']
                existing_bids = Bid.objects.filter(listing=listed)
                if not existing_bids:
                    if new_bid >= listed.starting_bid:
                        listed.starting_bid = new_bid
                        listed.save()
                        save_new_bid(bid_form, request.user, listed)
                    else:
                        messages.error(request, "The Bid Must Be Greater Than Or Equal To The Current Item Price.")
                        return HttpResponseRedirect(reverse('list_item', args=[title]))
                else:
                    highest_bid = bids.order_by('amount').last()
                    if new_bid > highest_bid.amount:
                        listed.starting_bid = new_bid
                        listed.save()
                        save_new_bid(bid_form, request.user, listed)
                    else:
                       messages.error(request, "The Bid Must Be Greater Than The Current Item Price.")
                       return HttpResponseRedirect(reverse('list_item', args=[title]))
            return HttpResponseRedirect(reverse("list_item", args=[title]))
             
        elif "submit_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                Comment = comment_form.save(commit=False)
                Comment.user = request.user
                Comment.listing = listed
                Comment.save()
                return HttpResponseRedirect(reverse("list_item", args=[title]))
    else:
        bid_form = BidForm()
        comment_form = CommentForm()

    
    bid_count = bids.count()
    highest_bid = bids.order_by('amount').last()
    coms = listed.coms.all()
    comment_count = coms.count()
    in_watchlist = Watchlist.objects.filter(user=request.user, listing=listed).exists()
    winner = highest_bid.user if highest_bid else None

    return render(request, "auctions/list_item.html", {
    "listed": listed,
    "bid_form": bid_form,
    "bid_count": bid_count,
    "highest_bid": highest_bid,
    "winner": winner,
    "new_bid": new_bid,
    "coms": coms,
    "comment_form": comment_form,
    "comment_count": comment_count,
    "in_watchlist": in_watchlist
    })

@login_required(login_url="login")
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })

def toggle_watchlist(request, title):
    listed = auction_listing.objects.get(title=title)
    watchlist_item = Watchlist.objects.filter(user=request.user, listing=listed)
    if not watchlist_item.exists():
        new_watchlist_item = Watchlist(user=request.user, listing=listed)
        new_watchlist_item.save()
    else:
        watchlist_item.delete()
    return HttpResponseRedirect(reverse("list_item", args=[title]))

def category(request):
    categories = auction_listing.category.field.choices
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def filter(request, category_name):
    listings = auction_listing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/filter.html", {
        "listings": listings,
        "category_name": category_name
    })