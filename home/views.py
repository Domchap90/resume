from django.shortcuts import render
from django.core.mail import send_mail

from django.contrib import messages
from .forms import ContactForm


def index(request):

    return render(request, 'home/index.html')


def about(request):

    return render(request, 'home/about.html')


def services(request):

    return render(request, 'home/services.html')


def portfolio(request):

    return render(request, 'home/portfolio.html')


def contact(request):
    form = ContactForm()

    if request.POST:
        print(f"")
        subject = "Message from contact page (DC webdeveloper)"
        message = "Message sent:\n\n" + request.POST["message"] + "\n\n\n\
Sent from: " + request.POST['name'] + "\nNumber given: \
" + request.POST.get("number", '')
        try:
            send_mail(subject, message,
                      request.POST.get("email"),
                      ['info@dc-webdeveloper.com'],
                      fail_silently=False)
            messages.success(request, "Thank you for getting in touch. Your\
 message has been sent.")
        except IOError:
            # Will catch both SMTPException AND socket.error
            messages.error(request, "Unable to send email at this time. Please try again\
later.")

    context = {
        'form': form,
    }

    return render(request, 'home/contact.html', context)
