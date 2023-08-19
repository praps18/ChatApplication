from django.urls import path
from . import views 


app_name='group'
urlpatterns = [
    path('/creategroup',views.create_group,name='creategroup'),
    path('/adduserstogroup',views.add_group,name="adduserstogroup"),
    path('/viewgroup/<int:id>/',views.viewgroup,name='groupview'),
    path('/viewmembers/',views.viewmembers,name='viewmembers'),
    path('/deletemembers',views.delete_member,name='delete_selected_members'),
     path('/user/search/',views.usersearch,name='usersearch'),
      path('editgroup/', views.edit_group, name='edit_group'),
    path('get_group_members/', views.get_group_members, name='get_group_members'),
    path('update_group_members/', views.update_group_members, name='update_group_members'),
]
