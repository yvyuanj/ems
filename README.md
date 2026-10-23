# 联通用户管理系统（EMS）— 自述文档

> 一个基于 **Django 4.2 + MySQL** 的后台用户管理 Web 系统（教学课程作业）。
> 覆盖「部门管理」「用户管理（普通表单 + ModelForm 两套实现）」「靓号管理」三大模块，
> 支持增删改查、关键词搜索、多条件筛选、列表分页、表单校验等完整后台功能。
> 代码做了分层重构：模型/表单/工具/视图分离，公共类和插件工具独立抽取，便于复用与讲解。

---

## 目录

1. 项目简介
2. 技术栈
3. 功能总览
4. 代码结构（分层设计）
5. 环境准备与安装
6. 运行启动
7. 数据库设计
8. 路由清单
9. 核心功能实现说明
   - 9.1 部门管理
   - 9.2 用户管理（普通表单）
   - 9.3 用户管理（ModelForm）
   - 9.4 靓号管理（搜索 + 筛选 + 校验 + 分页）
   - 9.5 列表分页（公共组件）
   - 9.6 公共类与工具抽取
10. 页面与样式
11. 常见问题与注意事项
12. 学习要点小结

---

## 1. 项目简介

模拟「联通用户管理系统」的后台业务，三个相互关联的数据模块：

| 模块 | 说明 |
| --- | --- |
| 部门管理 | 部门信息的增删改查 |
| 用户管理 | 用户信息增删改查，含普通表单版与 ModelForm 版两套实现 |
| 靓号管理 | 靓号（手机号）管理：手机号搜索、级别/状态筛选、格式校验、去重校验、分页 |

本项目完整覆盖 Django 核心链路：
**模型 Model → 视图 View → 模板 Template → 路由 URL → ORM 数据库**，
并在此基础上做了**分层重构**（`models.py / forms.py / utils.py / views.py` 职责分离）。

---

## 2. 技术栈

| 技术 | 版本 / 说明 |
| --- | --- |
| 后端框架 | Django 4.2 |
| 编程语言 | Python 3.x |
| 数据库 | MySQL（库名 `ems`） |
| ORM | Django 自带 ORM（makemigrations / migrate） |
| 模板引擎 | Django Template Language（DTL） |
| 前端 | 原生 HTML + 自定义 CSS（后台管理风格，无前端框架） |
| 分页 | Django 内置 `Paginator` + 通用分页组件 |
| 表单 | `request.POST` 普通写法 + 进阶 `ModelForm` |
| 校验 | `RegexValidator`（手机号格式）+ `clean_mobile`（去重） |

---

## 3. 功能总览

- **部门管理**：列表（分页）、新增、编辑、删除
- **用户管理**
  - 普通表单版：列表、新增、编辑、删除
  - ModelForm 版：自动生成表单、字段校验、错误回显
- **靓号管理**：列表、新增、编辑、删除
  - 按**手机号模糊搜索**（命中部分标红）
  - 按**级别 / 状态**组合筛选
  - **按级别从高到低排序**（与老师代码一致）
  - **手机号格式校验**（`1[3-9]\d{9}`）+ **手机号去重校验**
  - 列表**每页 3 条分页**，翻页保留筛选条件
- **通用分页组件**：首页 / 上一页 / 页码 / 下一页 / 尾页 / 页码跳转
- **分层重构**：表单类抽到 `forms.py`、工具函数抽到 `utils.py`，视图只写业务逻辑
- **统一后台布局**：顶部导航（部门 / 用户 / 靓号 下拉）、统一卡片 / 表格 / 表单样式

---

## 4. 代码结构（分层设计）

```
ems/
├── manage.py                 # Django 项目管理入口
├── ems/                      # 项目配置目录
│   ├── settings.py           # 全局配置（数据库、模板等）
│   ├── urls.py               # 全局路由
│   └── __init__.py           # 注册 PyMySQL
└── app01/                    # 业务应用
    ├── models.py             # ① 数据模型（部门/用户/靓号）
    ├── forms.py              # ② 公共表单类（UserModelForm / PrettyNumberModelForm）
    ├── utils.py              # ③ 插件工具（分页 / 手机号高亮 / 数字兜底）
    ├── views.py              # ④ 视图函数（只写业务逻辑，复用②③）
    ├── migrations/           # 数据库迁移文件
    └── templates/            # 页面模板
        ├── layout.html             # 公共母版（导航 + 样式）
        ├── pagination.html         # 通用分页组件
        ├── depart_list1.html       # 部门列表
        ├── depart_add1.html        # 新增部门
        ├── depart_edit1.html       # 编辑部门
        ├── user_list.html          # 用户列表
        ├── user_add.html           # 新增用户（普通）
        ├── user_edit.html          # 编辑用户（普通）
        ├── user_model_form_add.html# 新增用户（ModelForm）
        ├── user_model_form_edit.html# 编辑用户（ModelForm）
        ├── prettynum_list.html     # 靓号列表（搜索/筛选/分页）
        ├── prettynum_add.html      # 新增靓号（ModelForm）
        └── prettynum_edit.html     # 编辑靓号（ModelForm）
```

> **分层原则**：
> - `models.py`：只定义数据表结构
> - `forms.py`：把「基于模型的表单 + 校验规则」集中管理（公共类）
> - `utils.py`：把「分页、高亮、数字兜底」等通用函数集中管理（插件工具）
> - `views.py`：只负责取数、调用表单/工具、渲染页面（业务逻辑）

---

## 5. 环境准备与安装

### 5.1 需要的软件

- Python 3.x（建议 3.8+）
- Django 4.2：`pip install django==4.2`
- MySQL（本地，库名 `ems`）
- PyMySQL：`pip install pymysql`

### 5.2 数据库连接配置（`ems/settings.py`）

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ems",
        "USER": "root",
        "PASSWORD": "Root@123456",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

> 使用 PyMySQL 时，在 `ems/__init__.py` 中加入：
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

### 5.3 建表 / 迁移

表的两种来源：

1. **Django 自己建的表**（部门、用户）—— 执行迁移：
   ```bash
   python manage.py makemigrations app01
   python manage.py migrate
   ```
2. **已存在的表**（靓号表 `app_prettynum`）—— 直接映射，用 `--fake` 登记迁移记录：
   ```bash
   python manage.py migrate app01 0002_prettynumber --fake
   ```

---

## 6. 运行启动

```bash
python manage.py runserver 127.0.0.1:8000
```

浏览器访问：<http://127.0.0.1:8000/prettynum/list/>（或部门 / 用户列表）。

---

## 7. 数据库设计

共 3 张表：

### 7.1 `app01_department`（部门表）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | int (主键) | 自动生成 |
| title | varchar(32) | 部门名称 |

```python
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name='部门名称')
```

### 7.2 `app01_userinfo`（用户表）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | int (主键) | 自动生成 |
| name | varchar(16) | 姓名 |
| password | varchar(64) | 密码 |
| age | int | 年龄 |
| account | decimal(10,2) | 账户余额 |
| create_time | datetime | 入职时间 |
| gender | smallint | 性别（1=男，2=女） |
| depart | 外键 → department | 所属部门（级联删除） |

```python
class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='账号余额')
    create_time = models.DateTimeField(verbose_name='入职时间')
    depart = models.ForeignKey(to="Department", on_delete=models.CASCADE, verbose_name='所属部门')
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')
```

### 7.3 `app_prettynum`（靓号表）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | int (主键) | 自动生成 |
| mobile | varchar(11) | 手机号 |
| price | int (默认 0) | 价格 |
| level | smallint (默认 1) | 级别（1级/2级/3级） |
| status | smallint (默认 1) | 状态（1=已占用，2=未占用） |

```python
class PrettyNumber(models.Model):
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = ((1, "1级"), (2, "2级"), (3, "3级"))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = ((1, "已占用"), (2, "未占用"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    class Meta:
        db_table = "app_prettynum"   # 映射到已存在的表
```

> - **choices**：库里存数字，页面用 `get_xxx_display` 显示文字
> - **db_table**：让 Django 管理已存在的表，不重建

---

## 8. 路由清单（`ems/urls.py`）

### 部门管理

| URL | 视图 | 说明 |
| --- | --- | --- |
| `/depart/list/` | `depart_list` | 部门列表（分页） |
| `/depart/add/` | `depart_add` | 新增部门 |
| `/depart/delete/` | `depart_delete` | 删除部门（`?nid=xx`） |
| `/depart/<int:nid>/edit/` | `depart_edit` | 编辑部门 |

### 用户管理

| URL | 视图 | 说明 |
| --- | --- | --- |
| `/user/list/` | `user_list` | 用户列表（分页） |
| `/user/add/` | `user_add` | 新增用户（普通表单） |
| `/user/delete/` | `user_delete` | 删除用户（`?nid=xx`） |
| `/user/<int:nid>/edit/` | `user_edit` | 编辑用户（普通表单） |
| `/user/modelform/add/` | `user_model_form_add` | 新增用户（ModelForm） |
| `/user/modelform/edit/<int:nid>/` | `user_model_form_edit` | 编辑用户（ModelForm） |

### 靓号管理

| URL | 视图 | 说明 |
| --- | --- | --- |
| `/prettynum/list/` | `prettynum_list` | 靓号列表（搜索/筛选/排序/分页） |
| `/prettynum/add/` | `prettynum_add` | 新增靓号（ModelForm + 校验） |
| `/prettynum/delete/` | `prettynum_delete` | 删除靓号（`?nid=xx`） |
| `/prettynum/<int:nid>/edit/` | `prettynum_edit` | 编辑靓号（ModelForm + 去重校验） |

> 路由参数两种写法：
> - **路径参数** `<int:nid>`：`/prettynum/5/edit/`，视图形参 `nid`
> - **查询参数** `?nid=xx`：删除用，视图 `request.GET.get("nid")`

---

## 9. 核心功能实现说明

### 9.1 部门管理

部门表只有 title 一个业务字段，是理解 ORM「增删改查」的入门样例：

```python
# 查
def depart_list(request):
    queryset = Department.objects.all().order_by("id")
    page_obj, query_params = get_pagination(request, queryset)
    return render(request, "depart_list1.html", {"page_obj": page_obj, "query_params": query_params})

# 增
def depart_add(request):
    if request.method == "POST":
        Department.objects.create(title=request.POST.get("title"))
        return redirect("/depart/list/")

# 删
def depart_delete(request):
    nid = request.GET.get("nid")
    Department.objects.filter(id=nid).delete()

# 改
def depart_edit(request, nid):
    if request.method == "POST":
        Department.objects.filter(id=nid).update(title=request.POST.get("title"))
        return redirect("/depart/list/")
```

> ORM 四板斧：`.all()` 查全部 / `.create()` 增 / `.filter().update()` 改 / `.filter().delete()` 删。

### 9.2 用户管理（普通表单）

- 字段多、含外键（部门下拉）：视图把 `Department.objects.all()` 传给模板循环生成选项
- **数字字段空值兜底**：用 `int_or_default(...)` 工具，避免 MySQL 严格模式越界报错（DataError 1264）

```python
UserInfo.objects.create(
    name=request.POST.get("name"),
    age=int_or_default(request.POST.get("age")),   # 空值 → 0
    ...
)
```

### 9.3 用户管理（ModelForm）

ModelForm「根据模型自动生成表单 + 自动校验」，代码量更少更规范：

```python
# 公共类（forms.py）
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")   # 额外校验

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

# 视图只写流程（views.py）
def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()                          # 校验通过直接入库
        return redirect("/user/list/")
    return render(request, "user_model_form_add.html", {"form": form})  # 失败回显
```

### 9.4 靓号管理（搜索 + 筛选 + 校验 + 排序 + 分页）

最综合的一个模块：

```python
def prettynum_list(request):
    # ① 收集查询条件：有值才加，没值查全部
    data_dict = {}
    search_data = request.GET.get("q", "").strip()   # 手机号关键字
    level = request.GET.get("level", "").strip()
    status = request.GET.get("status", "").strip()
    if search_data: data_dict["mobile__contains"] = search_data   # LIKE '%..%'
    if level:       data_dict["level"] = level
    if status:      data_dict["status"] = status

    # ② 组合筛选 + 按级别降序 + 分页（公共工具）
    queryset = PrettyNumber.objects.filter(**data_dict).order_by("-level")
    page_obj, query_params = get_pagination(request, queryset)
    highlight_mobile(page_obj, search_data)      # 命中手机号标红
    ...
```

**靓号表单校验（`forms.py` 的 `PrettyNumberModelForm`）**：

```python
class PrettyNumberModelForm(forms.ModelForm):
    price = forms.IntegerField(required=False, initial=0, label="价格")
    # ① 手机号格式校验：1 开头、第二位 3-9、共 11 位
    mobile = forms.CharField(
        label="手机号", max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )
    class Meta:
        model = models.PrettyNumber
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        # ② 手机号去重（编辑时排除自己）
        txt = self.cleaned_data["mobile"]
        exists = models.PrettyNumber.objects.exclude(id=self.instance.pk).filter(mobile=txt).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt

    def clean_price(self):
        # ③ 价格空值兜底为 0
        return self.cleaned_data.get("price") or 0
```

### 9.5 列表分页（公共组件）

三个列表共用 Django `Paginator` + 通用组件 `pagination.html`：

```python
# 插件工具（utils.py）
def get_pagination(request, queryset, per_page=3):
    paginator = Paginator(queryset, per_page)                 # 每页 3 条
    page_obj = paginator.get_page(request.GET.get("page", 1)) # 当前页
    qs = request.GET.copy(); qs.pop("page", None)
    query_params = ("&" + qs.urlencode()) if qs else ""       # 保留搜索/筛选参数
    return page_obj, query_params
```

模板底部 `{% include "pagination.html" %}`，提供首页/上一页/页码/下一页/尾页/页码跳转，翻页自动保留筛选条件（如 `?page=2&q=156&level=1`）。

### 9.6 公共类与插件工具抽取（重构）

为减少重复、便于维护，把公共代码抽到两个模块：

| 模块 | 内容 | 类型 |
| --- | --- | --- |
| `forms.py` | `UserModelForm`、`PrettyNumberModelForm` | **公共类** |
| `utils.py` | `get_pagination`、`highlight_mobile`、`int_or_default` | **插件工具** |

- 三个列表视图的分页重复代码 → 一行 `get_pagination(...)`
- 靓号标红循环 → `highlight_mobile(...)`
- 数字字段 `or 0` 兜底 → `int_or_default(...)`
- 靓号新增/编辑从手写 POST 改为 `PrettyNumberModelForm`（与用户 ModelForm 同一套写法）

---

## 10. 页面与样式

- 公共母版 `layout.html`：顶部导航栏（部门/用户/靓号 均有下拉）、右上角登录用户、内容区卡片布局
- 统一后台风格：
  - 卡片面板 `.panel`、标题条 `.panel-title`
  - 表格隔行背景、hover 高亮
  - 按钮：绿色 `.btn-success`、蓝色 `.btn-edit`、红色 `.btn-del`、搜索 `.btn-search`
  - 表单控件 `.form-control`、错误提示 `.field-error`
  - 筛选表单 `.filter-form`、工具栏 `.toolbar`
  - 分页条 `.pagination / .page-btn / .page-info / .page-jump`

所有页面继承 `layout.html`，通过 `{% block content %}` 填充本页，可用 `{% block css %}` / `{% block js %}` 追加。

---

## 11. 常见问题与注意事项

1. **`DataError 1264`（数字越界）**：数字字段用 `int_or_default` 兜底，前端加 `required`。
2. **`DisallowedHost`**：`ALLOWED_HOSTS` 需放行访问域名/IP（测试时用 `HTTP_HOST='localhost'`）。
3. **模板报错**：`{% load static %}` 必须放在 `{% extends %}` 之后。
4. **分页警告 `UnorderedObjectListWarning`**：分页前 queryset 必须 `.order_by(...)`。
5. **已存在表**：映射预建表用 `migrate --fake`，不要重建。
6. **表单标签变英文**：重写 ModelForm 字段时必须显式 `label=`，否则丢掉 verbose_name（如 price→"Price"）。
7. **POST 重复提交**：写库成功后用 `redirect` 跳走。
8. **POST 表单 403**：表单内必须有 `{% csrf_token %}`。
9. **手机号校验**：格式不合法或重复，会在表单下方红字提示。

---

## 12. 学习要点小结

| 知识点 | 在项目的位置 |
| --- | --- |
| 模型 / 字段类型 / choices / 外键 / db_table | `models.py` |
| ORM 增删改查（all/create/filter/update/delete） | 各视图 |
| 视图 + 请求方法判断（GET/POST） | `views.py` |
| 路由 path 与路径参数 `<int:nid>` | `ems/urls.py` |
| 模板继承 extends / block / for / include | `templates/` |
| 表单提交 + csrf_token | 各 add/edit 模板 |
| ModelForm 自动生成与校验 | `forms.py` 的两个 ModelForm |
| 手机号格式校验（RegexValidator） | `PrettyNumberModelForm.mobile` |
| 手机号去重（clean_字段名） | `PrettyNumberModelForm.clean_mobile` |
| 动态条件组合查询 filter(**data_dict) | `prettynum_list` |
| 模糊搜索 __contains / mark_safe 高亮 | `highlight_mobile` |
| 分页 Paginator + 通用组件 | `utils.get_pagination` + `pagination.html` |
| 公共类 / 工具抽取重构 | `forms.py` / `utils.py` |

---

> 本文档随项目维护，用于课程讲解与复习。如有功能调整，请同步更新对应章节。
