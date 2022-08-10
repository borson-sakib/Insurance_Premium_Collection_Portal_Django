"""CharterIns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from telnetlib import LOGOUT
from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

    # path('', auth_views.LoginView.as_view()),
    # path('logout', auth_views.LogoutView.as_view(), name='logout'),
urlpatterns = [
    path('', login, name='home'),
    path('login', login, name='login') ,
    path('logout', logout, name='logout'),
    path('user_verify', index, name="landing"),
    path('verified', verify, name="verify_input"),
    path('registration', register, name="register"),
    # path('report', generate_report, name='report'),
    path('profile', getUserProfile, name="profile"),
    path('dae', dataverify, name="ss"),
    path('report', postdatabydate, name="report"),
    
    # path('txn_cnfrm', txn_confirm, name="transaction_confirmation"),
    # path('txn_cnfrm_success', txn_cnfrm_success, name="transaction_confirmation_success"),
    # path('txn_cnfrm_check', txn_confrm_check, name="transaction_confirmation"),
    # path('txn_cnfrm_check_success', txn_cnfrm_check_success, name="transaction_confirmation_success"),
    # path('login', login, name="bbb")
   

]
