from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from movie_app.models import Movie


class MovieViewSetTestClass(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create()
        self.movie = Movie.objects.create()

