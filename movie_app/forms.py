from django import forms
from movie_app.models import *
from django.core.exceptions import ValidationError


def is_too_easy(value):
    if value == '1234':
        raise ValidationError('Is too easy')
    return value


class SimpleForm(forms.ModelForm):
    rate = forms.IntegerField()

    class Meta:
        model = MovieRate
        fields = ('rate', 'movie')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SimpleForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(SimpleForm, self).clean()
        movie = data.get('movie')
        if MovieRate.objects.filter(user=self.user, movie=movie).exists():
            raise ValidationError(f'Movie rate with user {self.user.username} and movie {movie.title} already exists')
        return data

    def save(self, commit=True):
        instance = super(SimpleForm, self).save(commit=False)
        instance.user = self.user
        instance.save()
        return instance


class FormActor(forms.ModelForm):

    class Meta:
        model = MovieActor

        fields = (
            'name',
            'age',
        )

        labels = {
            'name': 'Name',
            'age': 'Age'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MovieRateForm(forms.ModelForm):
    """docstring for MovieRateForm"""
    
    def __init__(self, arg):
        super(MovieRateForm, self).__init__()
        self.arg = arg


class SearchMoviesForm(forms.Form):
    find_movies = forms.CharField()
