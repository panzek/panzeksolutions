from django import forms
from contact.models import Contact
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """
    Form for users to send company a message
    """

    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ('firstName',
                  'lastName',
                  'email',
                  'subject',
                  'message',
                  'captcha',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'firstName': 'Enter your first name',
            'lastName': 'Enter your last name',
            'email': 'Enter your email address',
            'subject': 'Enter your message subject',
            'message': 'Enter your message',
            'captcha': 'captcha',
        }

        self.fields['firstName'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control input-primary rounded max-w-full'
