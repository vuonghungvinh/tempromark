
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.text import wrap

from . import forms


def process_form(request):
    if request.method == 'POST':
        form = forms.ShareForm(request.POST, path=request.META['HTTP_REFERER'])
        if form.is_valid():
            _send_email(form.cleaned_data)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Thanks for sharing our website.'
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Page not shared: Ensure you have filled in all fields and try again.')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def _send_email(data):
    message = EmailMessage()
    message.subject = data.get('subject')
    message.body = wrap(
        render_to_string('share_page/email.txt', {'data': data}), 75)
    message.to = [data.get('to_address')]
    message.send()
