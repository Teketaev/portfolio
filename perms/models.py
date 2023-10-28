from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'

    def get_replies(self):
        return Comment.objects.filter(parent_comment=self).order_by('time_posted')


class BannedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.TextField()
    banned_by = models.ForeignKey(User, related_name='banned_users', on_delete=models.SET_NULL, null=True)
    banned_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=True)

    def __str__(self):
        return self.user
