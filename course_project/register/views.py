from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.db import IntegrityError
from personal_page.models import Account
from .forms import RegForm


def register(request):
    if request.POST:
        global form
        form = RegForm(request.POST)
        if form.is_valid():
            try:
                newbie = Account(
                    username = request.POST['username'],
                    email=request.POST['email'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name']
                )
                newbie.set_password(request.POST['password'])
                newbie.save()
                return HttpResponseRedirect(reverse('account', args=(newbie.id,)))
            except IntegrityError:
                form = RegForm()
                return render(request, 'register.html', {'error_message': 'This e-mail already exists!'})
    else:
        form = RegForm()
    return render(request, 'register.html', {'form': form})
# Create your views here.
