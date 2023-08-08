from django.urls import path
from . import views 


app_name='group'
urlpatterns = [
    path('/creategroup',views.create_group,name='creategroup'),
    path('/adduserstogroup',views.add_group,name="adduserstogroup"),
    path('/viewgroup/<int:id>/',views.viewgroup,name='groupview'),
    path('/viewmembers/',views.viewmembers,name='viewmembers'),
    path('/deletemembers',views.delete_member,name='delete_selected_members'),
     path('/user/search/',views.usersearch,name='usersearch')
]
