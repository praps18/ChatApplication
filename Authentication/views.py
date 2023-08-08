from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from group.models import Group
from django.contrib.auth.models import User



# Create your views here.
def home(request):
    return render(request,"index.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.username
            return redirect('userhome')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "login.html")

@login_required(login_url="/signin")
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

@login_required(login_url="/signin")
def getUserHomePage(request):
    user=User.objects.get(id=request.user.id)
    groups=user.group_set.all()
    name=request.user.username
    return render(request,'groups.html',{'fname':name,'usergroups':groups})