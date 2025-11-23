# job/widgets.py
from django import forms
from django.utils.safestring import mark_safe

class JSONEditorWidget(forms.Textarea):
    class Media:
        #js = ('https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.js',)
        js = (
            '/static/ace/ace.js',
            '/static/ace/mode-json.js',
            '/static/ace/theme-github.js',
        )

    def render(self, name, value, attrs=None, renderer=None):
        textarea = super().render(name, value, attrs, renderer)
        script = f"""
        <script>
            (function() {{
                var textarea = document.getElementById("id_{name}");
                if (!textarea) return;

                var editorDiv = document.createElement('div');
                editorDiv.style.width = "100%";
                editorDiv.style.height = "300px";
                textarea.style.display = "none";
                textarea.parentNode.insertBefore(editorDiv, textarea);

                var editor = ace.edit(editorDiv);
                editor.setTheme("ace/theme/github");
                editor.session.setMode("ace/mode/json");
                editor.setValue(textarea.value || '', -1);
                editor.session.on('change', function() {{
                    textarea.value = editor.getValue();
                }});
            }})();
        </script>
        """
        return mark_safe(textarea + script)
