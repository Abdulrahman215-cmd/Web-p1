import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CommentForm
from .models import User, SearchHistory, DirectionHistory, Comment, Profile

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
        history1 = DirectionHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
        username = request.user.username
        if history.count() > 5:
            oldest = history.last()
            oldest.delete()
        if history1.count() > 5:
            oldest1 = history1.last()
            oldest1.delete()
    else:
        history = []
        history1 = []
        username = None
    return render(request, 'Capstone/index.html', {
        'history': history,
        'history1': history1,
        'username': username,
        'theUser': request.user.username
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
            return HttpResponseRedirect(reverse("index"))  # Redirect to homepage or any other page
        else:
            return render(request, "Capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Capstone/login.html")
    



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
            return render(request, "Capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user) 
        except IntegrityError:
            return render(request, "Capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Capstone/register.html")


def search(request):
    if request.method == "POST":
        # CS50 ai told me to use json.loads
        query = json.loads(request.body).get("search-query")
        
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=query)
        return JsonResponse({'success': True})
    
    # Retrieve search history
    if request.user.is_authenticated:
        history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
        history_data = [{'query': h.query, 'timestamp': h.timestamp} for h in history]
    
    return JsonResponse({'success': False, 'history': history_data})

@login_required
def profile_page(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        return JsonResponse({"error": "username not found."}, status=404)
    has_commented = Comment.objects.filter(user=request.user, profile=profile).exists()
    if request.method == "POST":
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.profile = profile
                comment.review_type = request.POST.get('review_type')
                comment.save()
                messages.success(request, "Thank you for the review!")
                return HttpResponseRedirect(reverse("profile", args=[username]))
    else:
        if not has_commented:
           comment_form = CommentForm()
        else:
            comment_form = None

    Profile.objects.get_or_create(user=user)
    comment_count = Comment.objects.filter(profile=profile).count()
    good_review_count = Comment.objects.filter(profile=profile, review_type='Good').count()
    bad_reviews_count = Comment.objects.filter(profile=profile, review_type='Bad').count()
    comments = Comment.objects.filter(profile=profile).order_by('-date')
    # CS50 ai helped me in getting the percentage
    total_reviews = good_review_count + bad_reviews_count
    if total_reviews > 0:
        good_review_percentage = (good_review_count / total_reviews) * 100
    else:
       good_review_percentage = 0 

    return render(request, "Capstone/profile.html", {
        "profile": profile,
        "comment_form": comment_form,
        "comment_count": comment_count,
        "good_review_count": good_review_count,
        'bad_reviews_count': bad_reviews_count,
        "comments": comments,
        "current_user": request.user,
        "good_review_percentage": good_review_percentage,
    })


def get_directions(request):
    if request.method == "POST":
        start = json.loads(request.body).get("from")
        end = json.loads(request.body).get("to")
        

        DirectionHistory.objects.create(user=request.user, start_location=start, end_location=end)
        return JsonResponse({'success': True})
    
    history1 = DirectionHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
    history1_data = [{'start': h.start_location, 'end': h.end_location, 'timestamp': h.timestamp} for h in history1]
    
    return JsonResponse({'success': False, 'history1': history1_data})