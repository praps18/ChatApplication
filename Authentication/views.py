from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from group.models import CustomUser, Group
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


User = get_user_model()




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
    user=CustomUser.objects.get(id=request.user.id)
    groups=user.group_set.all()
    name=request.user.username
    return render(request,'groups.html',{'fname':name,'usergroups':groups})



def is_admin(user):
    return user.role =='admin'


@login_required(login_url="/signin")
def create_user(request):
    if not is_admin(request.user):
        raise  PermissionDenied("You're not authorised")
    if request.method=='GET':
        return render(request,'createuser.html')
    username = request.POST['username']
    password = request.POST['password']
    if username and password:
       user = User.objects.create_user(username=username, password=password)
       print("user saved")
    return redirect('createuser')   





@login_required(login_url="/signin")
def edit_user(request):
    if not is_admin(request.user):
        raise  PermissionDenied("You're not authorised")
    if request.method=='GET':
        users=CustomUser.objects.all()
        return render(request,'edituser.html',{'users':users})
    user_id = request.POST.get("user_id")
    username = request.POST.get("username")
    email = request.POST.get("email")
    user = get_object_or_404(CustomUser, id=user_id)
    user.username = username
    user.save()
    edited_user = CustomUser.objects.get(id=user_id)  # Replace with your code
    response_data = {
        'message': 'User edited successfully',
        'edited_username': edited_user.username,
    }
    return JsonResponse(response_data)   