from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('userhome',views.getUserHomePage,name='userhome'),
    path('createuser',views.create_user,name='createuser'),
    path('edituser',views.edit_user,name='edituser')
]