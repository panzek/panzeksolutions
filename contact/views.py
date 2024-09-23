from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm


def contact(request):
    """
    A view to render form in template
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            customer = form.save()
            contact_email = customer.email
            contact_subject = customer.subject
            contact_message = customer.message

            send_mail(
                contact_subject,  # subject
                contact_message,  # message
                contact_email,  # from email
                [settings.DEFAULT_FROM_EMAIL],  # to email
            )

            # redirect to a new url
            return redirect("/thank_you")

        else:
            # if form is not valid, re-render the form with errors
            template = 'contact/contact.html'
            context = {
                'form': form,
            }
            return render(request, template, context)

    else:
        form = ContactForm()

        template = 'contact/contact.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
