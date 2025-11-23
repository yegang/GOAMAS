from django.db import models

from django_ckeditor_5.fields import CKEditor5Field



class AlertCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    remark = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "告警分类"
        verbose_name_plural = "告警分类"

class AlertSeverity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default="#FF0000")
    icon = models.CharField(max_length=10, default="❗")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "告警等级"
        verbose_name_plural = "告警等级"


'''
字段	主要作用	场景
tags	用关键词组织告警、快速搜索、分组	“CPU、内存、磁盘”等标签
remark	人类可读备注，不影响逻辑	“临时模板”“测试专用”
source	标记模板来源系统	“system”“imported”“monitoring”
'''

class AlertContent(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field(verbose_name="告警内容")
    category = models.ForeignKey(AlertCategory, on_delete=models.SET_NULL, null=True, blank=True)
    severity = models.ForeignKey(AlertSeverity, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=(("enabled", "启用"), ("disabled", "禁用")),
        default="enabled"
    )
    tags = models.CharField(max_length=200, blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=100, default="system")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "告警内容"
        verbose_name_plural = "告警内容"
