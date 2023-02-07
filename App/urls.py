from django.urls import path
from App import  views

urlpatterns = [
    path('',views.Home, name='home'),
    path('login',views.Login, name='login'),
    path('register',views.Register, name='register'),
    path('logout',  views.Logout, name='logout'),
]