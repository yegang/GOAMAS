from django.db import models

# ① 通用 NotificationConfig （单例配置表）
class NotificationConfig(models.Model):
    """ 全局通知配置（email、qq、weixin 开关 + 通用配置） """

    market_time_limit = models.BooleanField(default=False)
    check_interval = models.IntegerField(default=900)

    # 标记是否启用
    email_enabled = models.BooleanField(default=True)
    qq_enabled = models.BooleanField(default=False)
    weixin_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "全局通知配置"
        verbose_name_plural = "全局通知配置"

    def __str__(self):
        return "全局通知配置"

# ② Email 配置表（OneToOne 单例）
class EmailConfig(models.Model):
    config = models.OneToOneField(NotificationConfig, on_delete=models.CASCADE)

    host = models.CharField(max_length=200)
    user = models.EmailField()
    password = models.CharField(max_length=200)
    sender = models.EmailField()
    title = models.CharField(max_length=200, default="通知标题")

    receivers = models.TextField(
        help_text="多个邮箱用英文逗号分隔"
    )

    class Meta:
        verbose_name = "Email 配置"
        verbose_name_plural = "Email 配置"

    def __str__(self):
        return "Email 配置"

# ③ QQ 配置表
class QQConfig(models.Model):
    config = models.OneToOneField(NotificationConfig, on_delete=models.CASCADE)

    api_url = models.CharField(max_length=300)
    qq_id = models.CharField(max_length=50)
    access_token = models.CharField(max_length=200)

    class Meta:
        verbose_name = "QQ 配置"
        verbose_name_plural = "QQ 配置"

    def __str__(self):
        return "QQ 配置"


# ④ 企业微信配置表（WeChat）
class WeixinConfig(models.Model):
    config = models.OneToOneField(NotificationConfig, on_delete=models.CASCADE)

    corp_id = models.CharField(max_length=100)
    agent_id = models.CharField(max_length=50)
    corp_secret = models.CharField(max_length=200)
    to_user = models.CharField(max_length=200, default="@all")

    class Meta:
        verbose_name = "企业微信配置"
        verbose_name_plural = "企业微信配置"

    def __str__(self):
        return "企业微信配置"


# ⑤ 股票监控表（多条数据）

class StockMonitor(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    buy_price = models.FloatField()
    sell_price = models.FloatField()

    class Meta:
        verbose_name = "股票监控配置"
        verbose_name_plural = "股票监控配置"

    def __str__(self):
        return f"{self.code} - {self.name}"
