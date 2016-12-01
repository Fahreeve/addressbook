from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authreg.forms import RegistrationForm


class UserCreateView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'registration.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data.get('password'))
        obj.save()
        return HttpResponseRedirect(reverse_lazy('login'))
