from django.contrib.auth import login
from django.urls import path, include
from movie_app.views import MovieAPIDetailView, MovieRateAPIListView,\
    MovieRateAPIDetailView, MovieLoginView, \
    MovieLogoutView
from .views import HomeView, MovieDetailView, MovieFormExample, ActorCreate
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('create_actor/', ActorCreate.as_view(), name='create_actor'),
    path('form/', MovieFormExample.as_view(), name='simple-form'),
    path('movie/', MovieAPIDetailView.as_view(), name='movie-list'),
    path('movie/<int:pk>/', MovieAPIDetailView.as_view(), name='movie-detail'),
    path('movie_rate/', MovieRateAPIListView.as_view(), name='movie-rate-list'),
    path('movie_rate/<int:pk>/', MovieRateAPIDetailView.as_view(), name='movie-rate-detail'),
    # path('movies/<slug>/', MovieDetailView.as_view(), name='movie-detail'),
    # path('movie/', MovieListView.as_view(), name='drf-movie-list'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('accounts/', include('django.contrib.auth.urls')),

    path('login/', MovieLoginView.as_view(), name='login'),
    path('logout/', MovieLogoutView.as_view(), name='logout'),
]
