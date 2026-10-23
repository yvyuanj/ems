"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("depart/list/", views.depart_list),  # 部门列表
    path("depart/add/", views.depart_add),  # 新增部门
    path("depart/delete/", views.depart_delete),  # 删除部门
    path("depart/<int:nid>/edit/", views.depart_edit),  # 编辑部门
    path("user/list/", views.user_list),  # 用户列表
    path("user/add/", views.user_add),  # 新增用户
    path("user/delete/", views.user_delete),  # 删除用户
    path("user/<int:nid>/edit/", views.user_edit),  # 编辑用户
    path("user/modelform/add/", views.user_model_form_add),  # 新增用户(ModelForm)
    path("user/modelform/edit/<int:nid>/", views.user_model_form_edit),  # 编辑用户(ModelForm)

    path("prettynum/list/", views.prettynum_list),  # 靓号列表（含搜索/筛选）
    path("prettynum/add/", views.prettynum_add),  # 新增靓号（GET表单/POST提交）
    path("prettynum/delete/", views.prettynum_delete),  # 删除靓号（?nid=xx）
    path("prettynum/<int:nid>/edit/", views.prettynum_edit),  # 编辑靓号（/prettynum/5/edit/）
]  # 编辑部门
