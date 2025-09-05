# job/forms.py
from django import forms
from .models import joblist
import json
from .widgets import JSONEditorWidget

class JobListForm(forms.ModelForm):
    class Meta:
        model = joblist
        fields = '__all__'
        widgets = {
            'args_list': JSONEditorWidget()
        }

    def clean_args_list(self):
        data = self.cleaned_data['args_list']
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, dict):
                raise forms.ValidationError("请输入 JSON 字典对象，例如：{\"ip\": \"127.0.0.1\"}")
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"JSON 格式错误：{str(e)}")
        return json.dumps(parsed)  # 确保存储格式一致
