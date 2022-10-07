from multiprocessing import context
from ssl import HAS_TLSv1_1
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Like_Post

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    context = {
        'user_profile':user_profile,
        'user_object':user_object,
        'posts':posts
    }
    return render(request,"social_book/index.html",context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        #checking if the passwords are the same and running a few conditionals. 
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"This email already exist, Try forgot password")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"This username already exist, Choose another")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
                user.save()

                # log user in and direct them to their profile
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                # create user profile object
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                messages.info(request,"Signup Successful!")
                return redirect('settings')
        else:
            messages.info(request,"Passwords didn't match")
            return redirect('signup')
    else:
        return render(request,"social_book/signup.html")

def signin(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # if the user exist
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request,'social_book/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    context ={
        'user_profile':user_profile
    }
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request,'social_book/settings.html',context)

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST['caption'] 

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return render(request,'social_book/upload.html')

@login_required(login_url='signin')
def edit_post(request,pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post
    }
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST['caption']
        if request.FILES.get("image") == None:
            post.caption = caption 
            post.save()
            return redirect('/')
        elif request.POST['caption'] == None:
            post.image = image
            post.save()
            return redirect('/')
        post.caption = caption 
        post.image = image
        post.save()
        return redirect('/')
    else:
        return render(request,'social_book/edit.html',context)

@login_required(login_url='signin')
def delete_post(request,pk):
    post = Post.objects.get(id=pk)
    context = {
            'post':post
        }
    if request.method == "POST":
        post.delete()
        return redirect('/')
    return render(request,'social_book/delete.html',context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    
    like_filter = Like_Post.objects.filter(post_id=post_id,username=username).first()

    if like_filter is None:
        new_like = Like_Post.objects.create(post_id=post_id, username=username)
        new_like.save() 
        post.num_likes += 1
        post.save()
        return redirect('/')
    else:
        remove_like = like_filter
        remove_like.delete()
        post.num_likes -= 1
        post.save()
        return redirect('/')

def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    context = {
        'user_profile' : user_profile,
        'user_object' :  user_object,
        'user_post' : user_post,
    }
    return render(request,'social_book/profile.html',context)



