from django.db import models

# ==================== 部门模型 ====================
# 部门表：只有名称字段
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.title


# ==================== 用户模型 ====================
# 用户表：用户基本信息 + 外键所属部门
class UserInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='账号余额')
    create_time = models.DateTimeField(verbose_name='入职时间')
    # 外键：一个用户属于一个部门，部门删除时用户一起删
    depart = models.ForeignKey(to="Department", on_delete=models.CASCADE, verbose_name='所属部门')
    # choices：库里存数字，页面用 get_gender_display 显示文字
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(choices=gender_choices, verbose_name='性别')

    def __str__(self):
        return self.name


# ==================== 靓号模型 ====================
# 靓号表：映射到已存在的表 app_prettynum
class PrettyNumber(models.Model):
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choices = ((1, "1级"), (2, "2级"), (3, "3级"))
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = ((1, "已占用"), (2, "未占用"))
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    def __str__(self):
        return self.mobile

    class Meta:
        # 指定用哪张数据库表
        db_table = "app_prettynum"


#python manage.py makemigrations
#python manage.py migrate
