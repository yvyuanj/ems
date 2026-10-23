"""
公共表单类（app01/forms.py）
所有基于模型的表单统一放这里，视图只负责调用，保持职责分离。
"""
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01 import models


# ==================== 用户表单 ====================
# 根据 UserInfo 模型自动生成控件，并做字段校验
class UserModelForm(forms.ModelForm):
    # 对 name 做额外校验：至少 3 个字
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        # 指定要渲染哪些字段
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]

    def __init__(self, *args, **kwargs):
        # 给所有控件统一加 form-control 样式和占位符
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
        # 入职时间用浏览器原生日期时间选择控件
        self.fields["create_time"].widget = forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control", "placeholder": "入职时间"},
            format="%Y-%m-%dT%H:%M",
        )


# ==================== 靓号表单 ====================
# 根据 PrettyNumber 模型自动生成控件（手机号/价格/级别/状态）
class PrettyNumberModelForm(forms.ModelForm):
    # 价格可不填，留空则默认 0（与原「or 0」兜底行为一致）
    # 注意：重写字段时需显式写 label，否则会丢掉模型里的 verbose_name，显示成 "Price"
    price = forms.IntegerField(required=False, initial=0, label="价格")

    # 手机号：重写字段 + 格式校验（1 开头、第二位 3-9、共 11 位）
    # 正则 ^1[3-9]\d{9}$ 对应国内手机号格式
    mobile = forms.CharField(
        label="手机号",
        max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNumber
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        # 与 UserModelForm 相同的样式处理：所有控件加 form-control 和占位符
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_price(self):
        # 价格为空的兜底：返回 0，避免入库 NULL
        return self.cleaned_data.get("price") or 0

    def clean_mobile(self):
        # 手机号去重校验：排除自己（编辑时），判断是否已存在
        txt_mobile = self.cleaned_data["mobile"]
        exists = (models.PrettyNumber.objects
                  .exclude(id=self.instance.pk)          # 编辑时排除当前这条
                  .filter(mobile=txt_mobile).exists())   # 是否有同号
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile
