from django.contrib import admin
from .models import (
    NotificationConfig,
    EmailConfig,
    QQConfig,
    WeixinConfig,
    StockMonitor,
)


# ===========================================================
# Inline 管理 Email / QQ / Weixin 配置
# ===========================================================

class EmailConfigInline(admin.StackedInline):
    model = EmailConfig
    extra = 0
    max_num = 1


class QQConfigInline(admin.StackedInline):
    model = QQConfig
    extra = 0
    max_num = 1


class WeixinConfigInline(admin.StackedInline):
    model = WeixinConfig
    extra = 0
    max_num = 1


# ===========================================================
# NotificationConfig 主配置
# ===========================================================

@admin.register(NotificationConfig)
class NotificationConfigAdmin(admin.ModelAdmin):
    """ 单例的全局通知配置 """
    inlines = [EmailConfigInline, QQConfigInline, WeixinConfigInline]

    list_display = ("id", "market_time_limit", "check_interval",
                    "email_enabled", "qq_enabled", "weixin_enabled")

    fieldsets = (
        ("基础参数", {
            "fields": ("market_time_limit", "check_interval")
        }),
        ("功能启用", {
            "fields": ("email_enabled", "qq_enabled", "weixin_enabled")
        }),
    )

    def has_add_permission(self, request):
        """ 限制只允许存在唯一一条配置 """
        return NotificationConfig.objects.count() == 0

    def changelist_view(self, request, extra_context=None):
        """ 如果没有配置，则自动创建一条，避免 admin 报错 """
        if NotificationConfig.objects.count() == 0:
            NotificationConfig.objects.create()
        return super().changelist_view(request, extra_context)


# ===========================================================
# 股票监控表
# ===========================================================

@admin.register(StockMonitor)
class StockMonitorAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "buy_price", "sell_price")
    search_fields = ("code", "name")
    list_filter = ("code",)
