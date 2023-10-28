from django.urls import path

from . import views

app_name = 'django_crud'

urlpatterns = [
    path('', views.MovieList.as_view(), name='movie_list'),
    path('movie-create/', views.MovieCreate.as_view(), name='movie_create'),
    path('movie-detail/<slug:slug>/', views.MovieDetail.as_view(), name='movie_detail'),
    path('movie-update/<slug:slug>/', views.MovieUpdate.as_view(), name='movie_update'),
    path('movie-delete/<slug:slug>/', views.MovieDelete.as_view(), name='movie_delete'),
]
