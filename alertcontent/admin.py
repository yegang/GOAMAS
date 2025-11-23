from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget


from .models import AlertContent, AlertCategory, AlertSeverity
from .resource import AlertContentResource
# Replace with your actual mixin import if you have a specific one.
try:
    from .mixins import CustomImportExportMixin
except Exception:
    class CustomImportExportMixin:  # fallback no-op
        pass

class AlertContentForm(forms.ModelForm):
    class Meta:
        model = AlertContent
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(),
        }

@admin.register(AlertCategory)
class AlertCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "remark")
    search_fields = ("name",)

@admin.register(AlertSeverity)
class AlertSeverityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "icon", "color")
    search_fields = ("name",)

@admin.register(AlertContent)
class AlertContentAdmin(CustomImportExportMixin, admin.ModelAdmin):
    resource_class = AlertContentResource
    form = AlertContentForm

    list_filter = ("category", "severity", "status", "source", "created_at")
    list_display = (
        "alert_icon",
        "id",
        "title",
        "category",
        "severity_icon",
        "colored_status",
        "preview_button",
        "copy_button",
        "test_send_button",
        "created_at",
    )
    search_fields = ("title", "content", "tags", "remark", "source")
    ordering = ("-created_at",)

    actions = ["action_enable", "action_disable", "action_copy"]

    change_form_template = "admin/alertcontent_change_form.html"

    # List icon
    def alert_icon(self, obj):
        return format_html('<span style="font-size:18px;">🔔</span>')
    alert_icon.short_description = ""

    # severity icon + colored label
    def severity_icon(self, obj):
        if not obj.severity:
            return "-"
        return format_html(
            '<span style="font-size:18px;">{icon}</span> '
            '<span style="color:white;background:{color};padding:3px 7px;border-radius:4px;">{name}</span>',
            icon=obj.severity.icon,
            color=obj.severity.color,
            name=obj.severity.name
        )
    severity_icon.short_description = "等级"
    severity_icon.admin_order_field = "severity"

    # status colored
    def colored_status(self, obj):
        color = "#2ecc71" if obj.status == "enabled" else "#7f8c8d"
        text = "启用" if obj.status == "enabled" else "禁用"
        return format_html(
            '<span style="color:white;background:{0};padding:3px 8px;border-radius:4px;">{1}</span>',
            color, text
        )
    colored_status.short_description = "状态"
    colored_status.admin_order_field = "status"

    # Preview button (opens bootstrap modal via JS)
    def preview_button(self, obj):
        return format_html(
            '<button type="button" class="button preview-btn" data-id="{id}" data-title="{title}">预览</button>',
            id=obj.id, title=obj.title
        )
    preview_button.short_description = "预览"

    # Copy button (link to duplicate view)
    def copy_button(self, obj):
        return format_html(
            '<a class="button" href="{url}">复制</a>',
            url=f"./{obj.id}/duplicate/"
        )
    copy_button.short_description = "复制"

    # Test send button
    def test_send_button(self, obj):
        return format_html(
            '<button type="button" class="button test-send-btn" data-id="{id}">测试发送</button>',
            id=obj.id
        )
    test_send_button.short_description = "测试发送"

    # Formfield customizations (category/severity choices display handled by FK admin)
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:obj_id>/preview/", self.admin_site.admin_view(self.preview_alert), name="alert_preview"),
            path("<int:alert_id>/duplicate/", self.admin_site.admin_view(self.duplicate_record), name="alert_duplicate"),
            path("<int:alert_id>/test_send/", self.admin_site.admin_view(self.test_send), name="alert_test_send"),
        ]
        return custom_urls + urls

    def preview_alert(self, request, obj_id):
        obj = get_object_or_404(AlertContent, id=obj_id)
        return JsonResponse({
            "title": obj.title,
            "content": obj.content,
            "category": str(obj.category) if obj.category else "",
            "severity": str(obj.severity) if obj.severity else "",
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def duplicate_record(self, request, alert_id):
        obj = get_object_or_404(AlertContent, id=alert_id)
        obj.pk = None
        obj.title = f"{obj.title}（复制）"
        obj.save()
        self.message_user(request, "复制成功")
        return redirect(f"../{obj.id}/change/")

    def test_send(self, request, alert_id):
        # NOTE: implement your actual send logic here (email/webhook/etc.)
        obj = get_object_or_404(AlertContent, id=alert_id)
        # For demo: just return success JSON
        return JsonResponse({"result": "ok", "msg": f"模拟发送: {obj.title}"})

    # Bulk actions
    def action_enable(self, request, queryset):
        updated = queryset.update(status="enabled")
        self.message_user(request, f"已启用 {updated} 条记录")
    action_enable.short_description = "批量启用"

    def action_disable(self, request, queryset):
        updated = queryset.update(status="disabled")
        self.message_user(request, f"已禁用 {updated} 条记录")
    action_disable.short_description = "批量禁用"

    def action_copy(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.title = f"{obj.title}（复制）"
            obj.save()
        self.message_user(request, "批量复制完成")
    action_copy.short_description = "批量复制"

    class Media:
        css = {
            "all": (
                "/static/admin/custom.css",  # 注意这里加了 /static/
            )
        }
        js = (
            "admin/bootstrap.bundle.min.js",   # include bootstrap bundle in your static
            "admin/alert_preview.js",
            "admin/ckeditor_var_highlight.js",
        )
