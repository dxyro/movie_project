from django.apps import AppConfig


class MovieAppConfig(AppConfig):
    name = 'movie_app'
    verbose_name = 'Django Movie Database'

    def ready(self):
        import movie_app.signals
