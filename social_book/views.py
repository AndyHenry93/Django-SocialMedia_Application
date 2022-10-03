from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    context = {
        'user_profile':user_profile
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

# @login_required(login_url='signin')
# def upload(request):
#     return render(request,'social_book/upload.html')