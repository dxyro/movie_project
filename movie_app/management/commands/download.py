import os

import requests
from django.core.management.base import BaseCommand
import datetime

from movie_app.models import MovieActor, MovieDirector, Country, Genre, Movie


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)

    def handle(self, *args, **options):

        def create_models(model, val, data, instance_list, idx):
            instance, get = model.objects.get_or_create(name=val, defaults=data)
            instance_list.append(instance)
            return instance_list

        pathurl = 'http://www.omdbapi.com/?'
        type = '&type=movie'
        if options['search']:
            search_type = 's='
        else:
            search_type = 't='
        title = options['title']
        apikey = '&apikey=545a0da2'
        url = pathurl+search_type+title+apikey+type
        r = requests.get(url)

        response = r.json()
        if response['Response'] == 'True':
            if response['Search']:
                for movie in response['Search']:
                    url = pathurl+'i='+movie['imdbID']+apikey+type
                    req = requests.get(url)
                    response_mo = req.json()
                    m_title = response_mo['Title']
                    m_country = response_mo['Country'].split(', ')
                    m_duration_list = response_mo['Runtime'].split(' min')[0]
                    if m_duration_list != 'N/A':
                        m_duration = int(m_duration_list)
                    else:
                        m_duration = 0
                    m_genre = response_mo['Genre'].split(', ')
                    m_director = response_mo['Director'].split(', ')
                    m_actors = response_mo['Actors'].split(', ')
                    m_original_language = response_mo['Language']
                    m_poster = response_mo['Poster']
                    m_detail = response_mo['Plot']
                    m_release = response_mo['Released']
                    if m_release == 'N/A':
                        m_release = '01 01 0001'
                        m_release_date = datetime.datetime.strptime(m_release, '%d %m %Y')
                    else:
                        m_release_date = datetime.datetime.strptime(m_release, '%d %b %Y')

                    instance = []

                    for idx, name in enumerate(m_actors):
                        defaults = {'name': name, 'age': None}
                        actors = create_models(MovieActor, name, defaults, instance, idx)
                    instance = []
                    for idx, name in enumerate(m_director):
                        defaults = {'name': name, 'age': None}
                        directors = create_models(MovieDirector, name, defaults, instance, idx)
                    instance = []
                    for idx, name in enumerate(m_country):
                        defaults = {'name': name}
                        countrys = create_models(Country, name, defaults, instance, idx)
                    instance = []
                    for idx, name in enumerate(m_genre):
                        defaults = {'name': name}
                        genres = create_models(Genre, name, defaults, instance, idx)

                    poster = None

                    if m_poster != 'N/A':
                        image = requests.get(m_poster)
                        try:
                            os.mkdir(f'media/movie/{m_title}_{m_release}/')
                        except:
                            pass
                        file_image = open(f'media/movie/{m_title}_{m_release}/{m_title}_{m_release}'
                                            f'.{m_poster.split(".")[-1]}',
                                            'wb'
                                         )
                        file_image.write(image.content)
                        file_image.close()
                        poster = '{}.{}'.format(m_title, m_poster.split('.')[-1])

                    defaults = {
                        'title': m_title, 'duration': m_duration, 'poster': poster,
                        'detail': m_detail, 'rating': None, 'release_date': m_release_date,
                        'original_language': m_original_language, 'country': countrys[0],
                    }
                    instance, get = Movie.objects.update_or_create(title=m_title, release_date=m_release_date,
                                                defaults=defaults)

                    instance.actors.add(*actors)
                    instance.director.add(*directors)
                    instance.genre.add(*genres)

                    instance.save()
        else:
            print(response['Error'])
