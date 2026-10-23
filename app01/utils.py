"""
插件工具（app01/utils.py）
与具体业务无关、可复用的通用函数都放这里，供视图调用。
"""
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe


# ==================== 分页工具 ====================
# 传入查询集和请求对象，返回 (当前页对象 page_obj, 保留的查询参数字符串 query_params)
# query_params 用于分页链接拼接，例如 ?page=2&q=156&level=1（已去掉 page 本身）
def get_pagination(request, queryset, per_page=3):
    paginator = Paginator(queryset, per_page)                    # 分页器：每页 per_page 条
    page_obj = paginator.get_page(request.GET.get("page", 1))    # 当前页（?page=xx，默认第 1 页）

    # 保留除 page 外的查询参数（搜索词、筛选条件等），翻页时不丢失
    qs = request.GET.copy()
    qs.pop("page", None)
    query_params = ("&" + qs.urlencode()) if qs else ""
    return page_obj, query_params


# ==================== 手机号高亮工具 ====================
# 把每行手机号里命中搜索词的部分标红，返回处理后的分页对象
def highlight_mobile(page_obj, search_data):
    for obj in page_obj:
        if search_data and search_data in obj.mobile:
            idx = obj.mobile.index(search_data)
            obj.mobile_hl = mark_safe(
                f"{obj.mobile[:idx]}<span style='color:#dd3737;'>{search_data}</span>{obj.mobile[idx + len(search_data):]}"
            )
        else:
            obj.mobile_hl = obj.mobile
    return page_obj


# ==================== 数字兜底工具 ====================
# 把表单提交的字符串转成整数；空值或非法值返回默认值，避免入库报错
def int_or_default(value, default=0):
    if value in (None, ""):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
