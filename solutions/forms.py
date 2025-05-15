from django import forms
from solutions.models import Solution
from django_ckeditor_5.widgets import CKEditor5Widget


class SolutionForm(forms.ModelForm):
    """
    Form for superuser to add, update, and delete Solutions
    """

    description = forms.CharField(
        widget=CKEditor5Widget(config_name='extends')
        )

    class Meta:
        model = Solution
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Solution name',
            'description': 'Solution Description',
            'tech_stack': 'Technologies used',
        }

        self.fields['name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            placeholder = placeholders.get(field, '')
            self.fields[field].widget.attrs['placeholder'] = placeholder

            # Only apply Tailwind/DaisyUi  styling to none-CKEditor fields
            if field != 'description':
                self.fields[field].widget.attrs['class'] = (
                    'form-control border-secondary input-primary rounded max-w-full'
                )
