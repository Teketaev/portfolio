from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('django-crud/', include('django_crud.urls', namespace='django_crud')),
    path('perms/', include('perms.urls', namespace='perms')),
    path('session_login/', views.CustomSessionLogin.as_view(), name='session_login'),
    path('logout/', LogoutView.as_view(next_page='session_login'), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
]