from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

class MultipleFileInput(ClearableFileInput):
    """
    A custom widget that extends ClearableFileInput to handle multiple file uploads.
    """
    template_name = 'foods/widgets/multiple_file_input.html'
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs.update({
            'multiple': True,
            'class': 'form-control',
            'accept': 'image/*'
        })
        self.attrs = attrs

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs'].update({
            'multiple': True,
            'class': 'form-control',
            'accept': 'image/*'
        })
        return context

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

    def value_omitted_from_data(self, data, files, name):
        return False 