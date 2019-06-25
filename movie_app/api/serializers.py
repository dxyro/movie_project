from rest_framework import serializers

from movie_app.models import MovieRate, Movie


class Movie2Serializer(serializers.ModelSerializer):
    # id = serializers.HyperlinkedIdentityField(view_name='drf-movie-detail')
    # title = serializers.CharField()
    # duration = serializers.IntegerField()
    # detail = serializers.CharField()
    # trailer_url = serializers.URLField()
    # rating = serializers.FloatField(default=5)
    # release_date = serializers.DateField()
    # original_language = serializers.CharField()
    # slug = serializers.CharField()
    # poster = serializers.ImageField()

    # def get_movie_rate(self, obj):
    #     rates = MovieRate.objects.get_rate_for_movie(obj)
    #     if rates.exists():
    #         return rates.first()['rate']
    #
    #     return ''

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster', 'duration', 'detail', 'trailer_url', 'rating', 'release_date',
                  'original_language', 'slug')


class MovieSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')
    poster = serializers.ImageField(read_only=True)
    trailer_url = serializers.URLField(required=False)

    class Meta:
        model = Movie
        fields = ('title',
                  'duration',
                  'poster',
                  'detail',
                  'trailer_url',
                  'genre',
                  'original_language',
                  'country',
                  'release_date', 'pk')


class MovieRateSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)
    # id = serializers.HyperlinkedIdentityField(view_name='movie_rate-detail-actions')
    user = serializers.StringRelatedField()
    # movie_link = serializers.HyperlinkedRelatedField(source='movie', read_only=True,
    #                                                  view_name='movie-detail-actions')
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieRate
        fields = ('movie', 'user', 'rate', 'pk')

