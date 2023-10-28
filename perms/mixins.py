from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import BannedUser


class CheckIfBannedMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                banned_user = BannedUser.objects.get(user=request.user)
                if banned_user.is_banned:
                    context = {
                        'reason': banned_user.reason,
                        'banned_by': banned_user.banned_by,
                        'banned_at': banned_user.banned_at,
                    }
                    return render(request, 'perms/banned.html', context)
            except BannedUser.DoesNotExist:
                pass

        return super().dispatch(request, *args, **kwargs)


class ModAdminOrPostOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.groups.filter(
            name__in=['admin', 'moderator']).exists()

    def handle_no_permission(self):
        return HttpResponse("You don't have permission to perform this action.", status=403)


class ModAdminOrMovieOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        movie = self.get_object()
        return self.request.user == movie.user or self.request.user.groups.filter(
            name__in=['admin', 'moderator']).exists()

    def handle_no_permission(self):
        return HttpResponse("You don't have permission to perform this action.", status=403)
