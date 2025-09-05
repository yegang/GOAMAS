from import_export.admin import ImportExportMixin
from django.core.exceptions import PermissionDenied

class CustomImportExportMixin(ImportExportMixin):
    def import_action(self, request, *args, **kwargs):
        if not request.user.has_perm('joblist.can_import_data'):  # 替换为你的导入权限
            raise PermissionDenied
        return super().import_action(request, *args, **kwargs)

    def export_action(self, request, *args, **kwargs):
        if not request.user.has_perm('joblist.can_export_data'):  # 替换为你的导出权限
            raise PermissionDenied
        return super().export_action(request, *args, **kwargs)