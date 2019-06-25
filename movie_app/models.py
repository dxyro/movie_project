import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from .choices import DEFAULTS, ORIGINAL_LANGUAGE, RATE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse_lazy
from .queryset import MovieRateQueryset

User = get_user_model()


def movie_directory_path(instance, filename):
    return f'movie/{instance.title}/{filename}'


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super(Genre, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)


class MovieActor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class MovieDirector(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    poster = models.ImageField(upload_to=movie_directory_path, null=True, blank=True)
    detail = models.TextField()
    trailer_url = models.URLField(null=True, blank=True)
    rating = models.FloatField(blank=True, null=True)
    release_date = models.DateField()
    original_language = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    director = models.ManyToManyField(MovieDirector)
    actors = models.ManyToManyField(MovieActor)
    genre = models.ManyToManyField(Genre)
    slug = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('movie-detail', args=(self.title, ))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title+str(self.release_date))
        super(Movie, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                update_fields=update_fields)


class MovieRate(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rate = models.FloatField()
    comment = models.TextField()
    objects = MovieRateQueryset.as_manager()

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f'{self.user.username} : {self.rate}'


class Tokenizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user
