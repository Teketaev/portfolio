from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from perms.mixins import CheckIfBannedMixin, ModAdminOrMovieOwnerMixin
from .forms import MovieForm
from .models import Movie, Genre, Category


class MovieList(ListView):
    model = Movie
    template_name = 'django_crud/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('genre').select_related('category', 'user')
        category_slug = self.request.GET.get('category')
        genre_slug = self.request.GET.get('genre')
        search_query = self.request.GET.get('search')
        only_title = self.request.GET.get('only_title')
        order_created = self.request.GET.get('order_created')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            queryset = queryset.filter(genre=genre)

        if search_query:
            if only_title:
                queryset = queryset.filter(title__icontains=search_query)
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

        if order_created == 'asc':
            queryset = queryset.order_by('time_created')
        elif order_created == 'desc':
            queryset = queryset.order_by('-time_created')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['categories'] = Category.objects.all()
        return context


class MovieCreate(CheckIfBannedMixin, LoginRequiredMixin, CreateView):
    model = Movie
    template_name = 'django_crud/movie_create.html'
    form_class = MovieForm
    context_object_name = 'form'
    success_url = reverse_lazy('django_crud:movie_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MovieDetail(DetailView):
    model = Movie
    template_name = 'django_crud/movie_detail.html'
    context_object_name = 'movie'


class MovieUpdate(CheckIfBannedMixin, LoginRequiredMixin, ModAdminOrMovieOwnerMixin, UpdateView):
    model = Movie
    template_name = 'django_crud/movie_update.html'
    context_object_name = 'form'
    form_class = MovieForm
    success_url = reverse_lazy('django_crud:movie_list')


class MovieDelete(CheckIfBannedMixin, LoginRequiredMixin, ModAdminOrMovieOwnerMixin, DeleteView):
    model = Movie
    template_name = 'django_crud/movie_delete_confirm.html'
    context_object_name = 'movie'
    success_url = reverse_lazy('django_crud:movie_list')
