from django.shortcuts import render

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

    context = {
        'form': form,
    }

    return render(request, 'home/contact.html', context)
