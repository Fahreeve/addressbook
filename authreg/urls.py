from django.conf.urls import url
from django.contrib.auth import views
from django.urls import reverse_lazy

from authreg.forms import MyAuthenticationForm
from authreg.views import UserCreateView

urlpatterns = [
    url(r'^login/$', views.login, {'template_name': 'login.html',
                                   'authentication_form': MyAuthenticationForm,
                                   'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': reverse_lazy('login')}, name='logout'),
    url(r'^registration/$', UserCreateView.as_view(), name='registration')
]
