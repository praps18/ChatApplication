from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required,login_required
from django.shortcuts import render
from .models import CustomUser, User
from django.shortcuts import render, redirect
from .models import Group,Message
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied




@login_required(login_url="/signin")
def create_group(request):
    users=CustomUser.objects.all()
    return render(request,"creategroup.html",{'users':users})




@login_required(login_url="/signin")
def add_group(request):
    if request.method == 'POST':
        name = request.POST['group_name']
        selected_user_ids = request.POST.getlist('selected_users')
        group = Group.objects.create(name=name,owner=request.user)
        group.members.set(selected_user_ids)
        return redirect('userhome')

    users = CustomUser.objects.all()
    return render(request, 'creategroup.html', {'users': users})

#todo only a authorised users should see this 
@login_required(login_url='/signin')
def viewgroup(request,id):
    print("view group")
    group=Group.objects.get(id=id)
    groups=request.user.group_set.all()
    print(groups)
    if not groups :
        raise PermissionDenied("You're not authorised")
    messages=Message.objects.filter(group=group)
    return render(request,'groupchat.html',{'group':group,'messages':messages,'user':request.user})


@login_required(login_url="/signin")
def viewmembers(request):
    print("i am view mmeners")
    id = request.GET.get("group_id")
    print(id)
    group = Group.objects.get(id=id)
    members = group.members.all()
    member_usernames = [member.username for member in members]
    return JsonResponse({"members":member_usernames})

# views.py


@csrf_protect
@require_POST
def delete_member(request):
    selected_members = request.POST.getlist("selected_members[]")
    print("the selected membets" + str(selected_members))
    group_id = request.POST.get("group_id")
    group = Group.objects.get(id=group_id)
    members_to_delete = CustomUser.objects.filter(username__in=selected_members)
    group.members.remove(*members_to_delete)
    #todo if the user selects his own name
    print(request.user.username in selected_members)
    if(request.user.username in selected_members):
        print("in if")
        return JsonResponse({"redirect": "userhome"})
    return JsonResponse({"message": "Selected members removed successfully"})




@login_required(login_url="/signin")
def usersearch(request):
    search_term = request.GET.get('q', '')
    print(search_term)
    users = CustomUser.objects.filter(username__icontains=search_term)[:10]
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse(user_list, safe=False)




@login_required(login_url="/signin")
def edit_group(request):
    return render(request, 'editexistinggroup.html')


@login_required(login_url="/signin")
def get_group_members(request):
    group_id = request.GET.get('group_id')
    group = Group.objects.get(pk=group_id)
    all_users = CustomUser.objects.all()

    checkboxes = []
    for user in all_users:
        checked = 'checked' if user in group.members.all() else ''
        checkboxes.append(f'<input type="checkbox" value="{user.id}" {checked}> {user.username}<br>')

    return JsonResponse({'checkboxes': checkboxes})


@login_required(login_url="/signin")
def update_group_members(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        users = request.POST.getlist('users[]')
        group = Group.objects.get(pk=group_id)

        group.members.set(users)

        return JsonResponse({'success': True})

    





