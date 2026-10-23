from django.shortcuts import render, redirect
from app01 import models
from app01.models import Department, UserInfo, PrettyNumber
from app01.forms import UserModelForm, PrettyNumberModelForm
from app01.utils import get_pagination, highlight_mobile, int_or_default


# ==================== 部门管理 ====================
# 部门列表：查出所有部门，按每页 3 条分页
def depart_list(request):
    queryset = Department.objects.all().order_by("id")
    page_obj, query_params = get_pagination(request, queryset)   # 公共工具：分页
    return render(request, "depart_list1.html", {"page_obj": page_obj, "query_params": query_params})


# 新增部门：POST 保存并跳回列表，GET 显示表单
def depart_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Department.objects.create(title=title)
        return redirect("/depart/list/")
    return render(request, "depart_add1.html")


# 删除部门：按 nid 删除后跳回列表
def depart_delete(request):
    nid = request.GET.get("nid")
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


# 编辑部门：POST 更新，GET 查出记录回显
def depart_edit(request, nid):
    if request.method == "POST":
        title = request.POST.get("title")
        Department.objects.filter(id=nid).update(title=title)
        return redirect("/depart/list/")
    row = Department.objects.filter(id=nid).first()
    return render(request, "depart_edit1.html", {"row_object": row})


# ==================== 用户管理 ====================
# 用户列表：按每页 3 条分页
def user_list(request):
    queryset = UserInfo.objects.all().order_by("id")
    page_obj, query_params = get_pagination(request, queryset)   # 公共工具：分页
    return render(request, "user_list.html", {"page_obj": page_obj, "query_params": query_params})


# 新增用户：POST 保存，GET 渲染表单（带上部门下拉）
def user_add(request):
    if request.method == "POST":
        # 数字字段用公共工具 int_or_default 兜底，避免空值报错
        UserInfo.objects.create(
            name=request.POST.get("name"),
            password=request.POST.get("password"),
            age=int_or_default(request.POST.get("age")),
            account=int_or_default(request.POST.get("account")),
            create_time=request.POST.get("create_time"),
            gender=int_or_default(request.POST.get("gender")),
            depart_id=int_or_default(request.POST.get("depart_id")),
        )
        return redirect("/user/list/")
    depart_list = Department.objects.all()
    return render(request, "user_add.html", {"depart_list": depart_list})


# 删除用户
def user_delete(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


# 编辑用户
def user_edit(request, nid):
    if request.method == "POST":
        UserInfo.objects.filter(id=nid).update(
            name=request.POST.get("name"),
            password=request.POST.get("password"),
            age=int_or_default(request.POST.get("age")),
            account=int_or_default(request.POST.get("account")),
            create_time=request.POST.get("create_time"),
            gender=int_or_default(request.POST.get("gender")),
            depart_id=int_or_default(request.POST.get("depart_id")),
        )
        return redirect("/user/list/")
    row = UserInfo.objects.filter(id=nid).first()
    depart_list = Department.objects.all()
    return render(request, "user_edit.html", {"row_object": row, "depart_list": depart_list})


# ==================== 用户 ModelForm 版本 ====================
# 新增用户（ModelForm）：GET 空表单，POST 校验后保存，失败回显错误
def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})


# 编辑用户（ModelForm）：GET 用 instance 回显，POST 校验后更新
def user_model_form_edit(request, nid):
    row = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row)
        return render(request, "user_model_form_edit.html", {"form": form})
    form = UserModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "user_model_form_edit.html", {"form": form})


# ==================== 靓号管理 ====================
# 靓号列表：按手机号/级别/状态组合筛选，命中手机号标红，每页 3 条分页
def prettynum_list(request):
    # 收集查询条件：有值才加，没值查全部
    data_dict = {}
    search_data = request.GET.get("q", "").strip()      # 手机号关键字
    level = request.GET.get("level", "").strip()        # 级别
    status = request.GET.get("status", "").strip()      # 状态
    if search_data:
        data_dict["mobile__contains"] = search_data     # __contains = LIKE '%..%'
    if level:
        data_dict["level"] = level
    if status:
        data_dict["status"] = status

    # 组合筛选 + 分页（按级别从高到低排序，与老师一致）
    queryset = PrettyNumber.objects.filter(**data_dict).order_by("-level")
    page_obj, query_params = get_pagination(request, queryset)   # 公共工具：分页（保留筛选参数）
    highlight_mobile(page_obj, search_data)                      # 公共工具：命中手机号标红

    return render(request, "prettynum_list.html", {
        "page_obj": page_obj,
        "search_data": search_data,
        "level": level,
        "status": status,
        "query_params": query_params,
    })


# 新增靓号（ModelForm）：GET 空表单，POST 校验后保存
def prettynum_add(request):
    if request.method == "GET":
        form = PrettyNumberModelForm()
        return render(request, "prettynum_add.html", {"form": form})
    form = PrettyNumberModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    return render(request, "prettynum_add.html", {"form": form})


# 删除靓号
def prettynum_delete(request):
    nid = request.GET.get("nid")
    PrettyNumber.objects.filter(id=nid).delete()
    return redirect("/prettynum/list/")


# 编辑靓号（ModelForm）：GET 用 instance 回显，POST 校验后更新
def prettynum_edit(request, nid):
    row = PrettyNumber.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNumberModelForm(instance=row)
        return render(request, "prettynum_edit.html", {"form": form})
    form = PrettyNumberModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/prettynum/list/")
    return render(request, "prettynum_edit.html", {"form": form})
