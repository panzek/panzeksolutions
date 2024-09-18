from django import forms
from contact.models import Contact
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """
    Form for users to send company a message
    """
    captcha = ReCaptchaField()
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Contact
        fields = ('first_name',
                  'last_name',
                  'email',
                  'subject',
                  'message',
                  'captcha',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter your first name',
            'last_name': 'Enter your last name',
            'email': 'Enter your email address',
            'subject': 'Enter your message subject',
            'message': 'Enter your message',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders:  # only set placeholder if the field is in a dictionary
                self.fields[field].widget.attrs['placeholder'] = placeholders[field]
                self.fields[field].widget.attrs['class'] = 'form-control input-primary rounded max-w-full'
