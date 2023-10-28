from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView, TemplateView

from .forms import PostForm, CommentForm, BanUserForm
from .mixins import CheckIfBannedMixin, ModAdminOrPostOwnerMixin
from .models import Post, Comment, BannedUser


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'perms/post_list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_mod_or_admin'] = self.request.user.groups.filter(
            name__in=['admin', 'moderator']).exists()
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author')
        return queryset


class PostCreateView(CheckIfBannedMixin, LoginRequiredMixin, CreateView):
    model = Post
    context_object_name = 'form'
    template_name = 'perms/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('perms:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(CheckIfBannedMixin, LoginRequiredMixin, DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'perms/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = self.request.user
            comment.post = post
            parent_comment_id = self.request.POST.get('parent_comment', None)
            if parent_comment_id:
                comment.parent_comment_id = parent_comment_id
            comment.save()
            return redirect('perms:post_detail', pk=post.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author')
        return queryset


class PostUpdateView(CheckIfBannedMixin, LoginRequiredMixin, ModAdminOrPostOwnerMixin, UpdateView, ):
    model = Post
    context_object_name = 'form'
    template_name = 'perms/post_update.html'
    form_class = PostForm
    success_url = reverse_lazy('perms:post_list')


class PostDeleteView(CheckIfBannedMixin, LoginRequiredMixin, ModAdminOrPostOwnerMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    template_name = 'perms/post_delete.html'
    success_url = reverse_lazy('perms:post_list')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.comments.all().delete()
        post.delete()
        return HttpResponseRedirect(self.success_url)


class CommentDeleteView(CheckIfBannedMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        comment = self.get_object()
        return reverse('perms:post_detail', args=[comment.post.pk])


@method_decorator(login_required, name='dispatch')
class BanUserView(CheckIfBannedMixin, LoginRequiredMixin, TemplateView):
    template_name = 'perms/ban_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        context['form'] = BanUserForm()
        return context

    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if not request.user.groups.filter(name__in=['moderator', 'admin']).exists():
            messages.error(request, 'You do not have permission to Ban users.')
            return redirect('perms:ban_user', user_id=user_id)

        form = BanUserForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']

            if user.groups.filter(name__in=['moderator', 'admin']).exists():
                messages.error(request, 'Admins and Moderators cannot be banned.')
                return redirect('perms:ban_user', user_id=user_id)
            else:
                banned_user, created = BannedUser.objects.get_or_create(user=user)
                banned_user.is_banned = True
                banned_user.reason = reason
                banned_user.banned_by = request.user
                banned_user.save()
                messages.success(request, f'User [{user.username}] has been banned.')
            return redirect('perms:ban_user', user_id=user_id)

        return redirect('perms:ban_user', user_id=user_id)


@method_decorator(login_required, name='dispatch')
class UnbanUserView(CheckIfBannedMixin, LoginRequiredMixin, TemplateView):
    template_name = 'perms/unban_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        context['user'] = user
        return context

    def post(self, request, user_id):
        if not request.user.groups.filter(name__in=['moderator', 'admin']).exists():
            messages.error(request, 'You do not have permission to ban or unban users.')
            return redirect('perms:unban_user', user_id=user_id)

        user = get_object_or_404(User, id=user_id)

        try:
            banned_user = BannedUser.objects.get(user=user)
            banned_user.is_banned = False
            banned_user.save()
            messages.success(request, f'User [{user.username}] has been unbanned.')
        except BannedUser.DoesNotExist:
            messages.error(request, f'User [{user.username}] cannot be found')

        return redirect('perms:unban_user', user_id=user_id)
