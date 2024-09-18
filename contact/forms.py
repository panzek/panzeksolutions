from django import forms
from contact.models import Contact
from django_recaptcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
import re


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

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("First name should contain only letters")
        if len(first_name) < 3:
            raise ValidationError('First name should be at least 3 characters long')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Last name should contain only letters")
        if len(last_name) < 3:
            raise ValidationError('Last name should be at least 3 characters long')
        return last_name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise ValidationError('Message should be at least 10 characters long')
        return message

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format. Please enter valid email address")
        return email
