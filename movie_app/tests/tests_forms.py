from django.contrib.auth.models import User
from django.forms import forms
from django.test import TestCase
from movie_app.forms import SimpleForm
from movie_app.models import Movie, MovieRate


'''class ExceptionContext:
    def __init__(self):
        self.assertion = False
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        assertion = exc_type is not None
        assert assertion'''


class SimpleFormTestCase(TestCase):
    rate = forms.IntegerField()

    def setUp(self) -> None:
        self.user = User.objects.create(username='dxyro', email='chxmorro@gmail.com')
        self.movie = Movie.objects.create(title='wonder woman', duration=100, original_language='EN', country='USA')
        self.form = SimpleForm(user=self.user, data={'rate': 1, 'movie': self.movie.id, 'user': self.user})

    def test_simple_form_should_return_data_if_any_movierate_exist_for_user_and_movie(self):
        self.form.is_valid()
        data = self.form.clean()
        self.assertEqual(data, {'rate': 1, 'movie': self.movie.id})
