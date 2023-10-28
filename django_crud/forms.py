from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['category', 'genre', 'title', 'slug', 'description', 'image']