import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .forms import All_PostsForm
from .models import User, All_Posts, Follow, Like

def paginate(request, queryset):
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def index(request):
    posts = All_Posts.objects.all().order_by("-timestamp")
    for post in posts:
        post.like_count = Like.objects.filter(lik=post).count()
        if request.user.is_authenticated:
            post.user_liked = Like.objects.filter(lik=post, liker=request.user).exists()
        else:
            # cs50 ai told me what to put exactly in the else:
            post.user_liked = False
    page_obj = paginate(request, posts)
    
    if request.method == "POST":
        if request.user.is_authenticated:
            form = All_PostsForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.poster = request.user
                new_post.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        form = All_PostsForm()
    
    return render(request, "network/index.html", {
        "form": form,
        "page_obj": page_obj,
    })

@csrf_exempt
def update_post(request, post_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        new_post = data.get('newPost', '').strip()

        try:
            post = All_Posts.objects.get(id=post_id)
            if post.poster == request.user:
                post.NewPost = new_post
                post.save()
                return JsonResponse({"message": "Post updated successfully."}, status=200)
            else:
                return JsonResponse({"error": "Unauthorized."}, status=403)
        except All_Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
    



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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile_page(request, username):
    try:
        profile = User.objects.get(username=username)
        posts = All_Posts.objects.filter(poster=profile).order_by('-timestamp')
        followers_count = profile.followers.count()
        following_count = profile.following.count()
        posts_count = posts.count()
        for post in posts:
            post.like_count = Like.objects.filter(lik=post).count()
            if request.user.is_authenticated:
                post.user_liked = Like.objects.filter(lik=post, liker=request.user).exists()
            else:
                post.user_liked = False
        page_obj = paginate(request, posts)
        if request.user.is_authenticated:
            is_following = Follow.objects.filter(follower=request.user, foll=profile).exists()
        else:
            is_following = False
    except User.DoesNotExist:
        return JsonResponse({"error": "username not found."}, status=404)
    return render(request, "network/profile.html", {
        "profile": profile,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count,
        "page_obj": page_obj,
    })


def follow(request):
    # cs50 ai told helped me in followed users, turns out flat=True is easier and faster then making a seperate variable
    followed_users = Follow.objects.filter(follower=request.user).values_list('foll', flat=True)
    posts = All_Posts.objects.filter(poster__in=followed_users).order_by('-timestamp')
    for post in posts:
        post.like_count = Like.objects.filter(lik=post).count()
        post.user_liked = Like.objects.filter(lik=post, liker=request.user).exists()
    page_obj = paginate(request, posts)
    return render(request, "network/follow.html", {
        "followed_users": followed_users,
        "page_obj": page_obj,
    })

def toggle_follow(request, username):
    followed = User.objects.get(username=username)
    follow = Follow.objects.filter(follower=request.user, foll=followed)
    if not follow.exists():
        new_follow = Follow(follower=request.user, foll=followed)
        new_follow.save()
    else:
        follow.delete()
    return HttpResponseRedirect(reverse("profile", args=[username]))

def toggle_like(request, post_id):
    try:
        post = All_Posts.objects.get(id=post_id)
        # get_or_create was the help of cs50 ai, i didnt know it existed
        like, created = Like.objects.get_or_create(liker=request.user, lik=post)
    
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Like.objects.filter(lik=post).count()
        return JsonResponse({'liked': liked, 'like_count': like_count})
    except All_Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
  