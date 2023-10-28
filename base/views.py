import logging

from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import RegistrationForm

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'base/home.html'


class CustomSessionLogin(LoginView):
    template_name = 'base/session_login.html'

    def get_success_url(self):
        username = self.request.user.username
        logger.info(f"User {username} logged in successfully.")
        return reverse_lazy('home')


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'base/registration.html'
    context_object_name = 'form'
    success_url = reverse_lazy('session_login')

    def form_valid(self, form):
        user = form.save()

        default_user_group, created = Group.objects.get_or_create(name='default_user')
        user.groups.add(default_user_group)

        logger.info(f"User {user.username} registered successfully.")

        return super().form_valid(form)
