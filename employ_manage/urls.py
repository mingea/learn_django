"""employ_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from app01 import views
from userinfo import views as user_views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("index/",views.index),
    path("depart/list/",views.depart_list),
    path("depart/add/",views.depart_add),
    path("depart/edit/<int:nid>/",views.depart_edit),
    path("depart/delete/<int:nid>/",views.depart_del),
    path("employee/add/",views.employee_add),
    path("employee/list/",views.employee_list),
    path('employee/edit/<int:nid>/',views.employee_edit),
    path('employee/delete/<int:nid>/',views.employee_del),
    path('familymember/list/',views.familymember_list),
    path('familymember/add/',views.familymember_add),
    path('familymember/edit/<int:nid>/',views.familymember_edit),
    path('familymember/delete/<int:nid>/',views.familemember_del),
    path("user/list/",user_views.user_list),
    path("user/logout/",user_views.user_logout),
    path("user/reset/",user_views.reset_password),
    path("",user_views.user_login),#根路径
    path("user/logout/",user_views.user_logout),
    path("user/add/",user_views.user_add),
    path("image/code/",user_views.get_catpcha),
    path("changePassword/",user_views.change_password),

]
