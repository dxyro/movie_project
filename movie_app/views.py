from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, RedirectView
from django.urls import reverse_lazy
from django.views.generic.list import BaseListView
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from movie_app.api.serializers import MovieSerializer, MovieRateSerializer
from movie_app.forms import FormActor, SearchMoviesForm
from django.contrib.auth.mixins import LoginRequiredMixin

from movie_app.models import Tokenizer, Suggest
from movie_app.tasks import emails, call_command_task
from .forms import SimpleForm
from .models import MovieRate, Movie, MovieActor
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import login, logout
from uuid import uuid4

# Create your views here.


class ActorCreate(CreateView):
    model = MovieActor
    form_class = FormActor
    template_name = 'movie_app/create_actor.html'
    success_url = reverse_lazy('movie_app:create_actor')


class HomeView(ListView):
    template_name = 'movie_app/home.html'
    extra_context = {'title': 'My Internet movie database'}
    queryset = Movie.objects.all()
    paginate_by = 6

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        best_movie = MovieRate.objects.get_best_rated().first()
        if best_movie:
            movie = Movie.objects.get(pk=best_movie.get('movie'))
            data.update({
                'best_rated_movie': movie,
                'best_rated_value': best_movie.get('rate', 0),
            })
            return data


class MovieDetailView(LoginRequiredMixin, DetailView):
    queryset = Movie.objects.all()
    template_name = 'movie_app/detail.movie.html'
    slug_field = 'slug'
    query_pk_and_slug = False


class MovieFormExample(CreateView):
    template_name = 'movie_app/simple.form.example.html'
    form_class = SimpleForm
    success_url = '.'

    def form_invalid(self, form):
        return super(MovieFormExample, self).form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(MovieFormExample, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class MovieJson(BaseListView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, object_list=None, **kwargs):
        context = super(MovieJson, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieSerializer(self.get_queryset(), many=True).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class DetailMovieJson(DetailView):
    model = Movie
    content_type = 'application/json'
    response_class = HttpResponse

    def get_context_data(self, object_list=None, **kwargs):
        context = super(DetailMovieJson, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'serialized_data': JSONRenderer().render(MovieSerializer(self.get_object()).data)})
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            context.get('serialized_data'), **response_kwargs
        )


class MovieAPIListView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRateAPIListView(ListCreateAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieRateAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'movie_app/registration/login.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # tokenizer = Tokenizer(user=request.user)
            # tokenizer.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(MovieLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        token = Token.objects.create(user=self.request.user)
        return super(MovieLoginView, self).form_valid(form)


class MovieLogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        # tokenizer = Tokenizer.objects.get(user=request.user)
        token = Token.objects.get(user=request.user)
        token.delete()
        # tokenizer.delete()
        logout(request)
        return super(MovieLogoutView, self).get(request, *args, **kwargs)


class SearchMoviesView(FormView):
    form_class = SearchMoviesForm
    template_name = 'movie_app/search.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        suggest = Suggest.objects.all()
        if form.data['find_movies']:
            data_list = form.data['find_movies'].split(', ')
            for data in data_list:
                suggest.get_or_create(suggest=data)
        return super().form_valid(form)

