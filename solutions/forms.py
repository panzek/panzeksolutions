from django import forms
from solutions.models import Solution


class SolutionForm(forms.ModelForm):
    """
    Form for superuser to add, update, and delete Solutions
    """

    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

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
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control border-secondary input-primary rounded max-w-full'
