from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm


def contact(request):
    """
    A view to render form in template
    """

    # ContactForm(request.POST)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            customer_message = form.save()
            contact_email = customer_message.email
            contact_subject = customer_message.subject
            contact_message = customer_message.message

            send_mail(
                contact_subject,  # subject
                contact_message,  # message
                contact_email,  # from email
                [settings.DEFAULT_FROM_EMAIL],  # to email
            )

            # redirect to a new url
            return redirect("/thank_you")

    else:
        form = ContactForm()

        template = 'contact/contact.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
