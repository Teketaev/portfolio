from django import forms

from .models import Post, Comment, BannedUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'allow_comments']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent_comment']
        widgets = {
            'parent_comment': forms.HiddenInput(),
        }


class BanUserForm(forms.ModelForm):
    class Meta:
        model = BannedUser
        fields = ['reason']
