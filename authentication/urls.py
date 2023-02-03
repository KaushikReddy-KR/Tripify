"""tripify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('dash/', views.dashboard, name='dash'),
    path('create-journ/', views.createJourn, name='create-journ'),
    path('update-journ/<str:pk>/', views.updateJourn, name='update-journ'),
    path('delete/<str:pk>/', views.deleteJourn, name='delete-journ'),

    path('chat-home/', views.chat_home, name='chat1-home'),
    path('login/', auth_views.LoginView.as_view(template_name="authentication/login.html"), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="authentication/logout.html"), name='chat-logout'),
    path('register/', views.register, name='chat-register'),
    path('home/', views.chat_home, name='chat-home'),
    path('profile/', views.profile, name='chat-profile'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
]
