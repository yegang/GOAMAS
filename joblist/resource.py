from import_export import resources

from .models import joblist



class joblistResource(resources.ModelResource):
    class Meta:
        model = joblist

        fields = (
            'decpet',
            'job_name',
            'trigger_name',
            'type_choices',
            'type_content',
            'action_type',
            'gender_choices',
            'job_state',
            'job_rate',
            'time'
        )
        #exclude = ('id')
        export_order = (
            'decpet',
            'job_name',
            'trigger_name',
            'type_choices',
            'type_content',
            'action_type',
            'gender_choices',
            'job_state',
            'job_rate',
            'time'
        )
        import_order = (
            'decpet',
            'job_name',
            'trigger_name',
            'type_choices',
            'type_content',
            'action_type',
            'gender_choices',
            'job_state',
            'job_rate',
            'time'
        )

