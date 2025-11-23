from import_export import resources, fields
from import_export.widgets import DateTimeWidget
from .models import AlertContent

class AlertContentResource(resources.ModelResource):
    created_at = fields.Field(attribute="created_at", column_name="created_at",
                              widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"))
    updated_at = fields.Field(attribute="updated_at", column_name="updated_at",
                              widget=DateTimeWidget(format="%Y-%m-%d %H:%M:%S"))

    class Meta:
        model = AlertContent
        fields = (
            "id","title","content","category","severity","status",
            "tags","remark","source","created_at","updated_at"
        )
        import_id_fields = ("id",)
        export_order = fields
