import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

from .form_classes import NewPost

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    p = Paginator(posts, 10)
    pages_num = p.num_pages
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            new_post = Post(user=request.user, text=text)
            new_post.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "network/index.html", {
                "form": form,
                "pages_num": pages_num
            })
    return render(request, "network/index.html", {
        "form": NewPost(),
        "pages_num": pages_num
    })

@register.filter
def get_range(value):
    return range(value)

def posts(request, pg):
    try:
        name = request.GET["user"]
        user = User.objects.get(username=name)
        posts = Post.objects.filter(user=user).order_by("-date")
    except:
        posts = Post.objects.all().order_by("-date")
    p = Paginator(posts, 10)
    try:
        page = p.page(pg)
    except EmptyPage:
        return JsonResponse({"error": "No page exists"}, status=404)
    return JsonResponse([post.serialize() for post in page], safe=False, status=201)

@login_required
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        id = int(data["id"])
        text = data["text"]
        try:
            post = Post.objects.get(pk=id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Object does not exist"}, status=404)
        if request.user == post.user:
            post.text = text
            post.save()
            return JsonResponse({"success": "Operation successful"}, status=201)
        return JsonResponse({"success": "Incorrect user"}, status=403)

@login_required
def follow(request, user):
    if request.method == "PUT":
        data = json.loads(request.body)
        follow = data["follow"]
        user = User.objects.get(username=user)
        if follow:
            user.followers.add(request.user)
        else:
            user.followers.remove(request.user)
        return JsonResponse({"success": "Operation successful."}, status=201)

@login_required
def like(request, post_id):
    if request.method == "PUT":
        user = request.user
        data = json.loads(request.body)
        like = data["like"]
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Object does not exist"}, status=404)
        if like:
            post.likers.add(user)
        else:
            post.likers.remove(user)
        likes = post.likers.all().count()
        return JsonResponse({"likes": likes}, status=201)


def user(request):
    name = request.GET["name"]
    user = User.objects.get(username=name)
    posts = Post.objects.filter(user=user)
    p = Paginator(posts, 10)
    pages_num = p.num_pages
    is_followed = False 
    followers = user.followers.all().count()
    followed = User.objects.filter(followers=user).count()
    for follower in user.followers.all():
        if follower == request.user:
            is_followed = True
    return render(request, "network/user.html", {
        "profiled_user": user,
        "is_followed": is_followed,
        "followers": followers,
        "followed": followed,
        "pages_num": pages_num
    })

@login_required
def following_posts(request, pg):
    user = request.user
    following = User.objects.filter(followers=user)
    all_posts = []
    for followed in following:
        posts = Post.objects.filter(user=followed).order_by("-date")
        [all_posts.append(post) for post in posts]
    p = Paginator(all_posts, 10)
    try:
        page = p.page(pg)
    except EmptyPage:
        return JsonResponse({"error": "No page exists"}, status=404)
    return JsonResponse([post.serialize() for post in page], safe=False, status=201)

@login_required
def following(request):
    user = request.user
    following = User.objects.filter(followers=user)
    is_following = True if following else False
    all_posts = []
    for followed in following:
        posts = Post.objects.filter(user=followed).order_by("-date")
        [all_posts.append(post) for post in posts]
    p = Paginator(all_posts, 10)
    pages_num = p.num_pages
    return render(request, "network/following.html", {
        "is_following": is_following,
        "pages_num": pages_num
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