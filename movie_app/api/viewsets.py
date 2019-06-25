from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK

from movie_app.api.filters import MovieFilterSet
from movie_app.api.paginators import StandarResultsSetPagination
from movie_app.api.permissions import IsAuthenticatedOrReadOnlyCustom
from movie_app.api.serializers import MovieRateSerializer, MovieSerializer
from movie_app.models import MovieRate, Movie


class Example2Viewset(viewsets.ViewSet):
    model = MovieRate
    serializer_class = MovieRateSerializer

    def get_queryset(self):
        _filter = {}
        if 't' in self.request.query_params.keys():
            _filter.update({'movie__title__icontains': self.request.query_params.get('t')})
        if 'u' in self.request.query_params.keys():
            _filter.update({'user__username__icontains': self.request.query_params.get('u')})
        return self.model.objects.filter(**_filter)

    def get_object(self, pk):
        return get_object_or_404(self.get_queryset(), pk=pk)

    def get_serializer(self, query, many=False):
        return MovieRateSerializer(query, many=many, context={'request': self.request})

    def list(self, request):
        qs = self.get_queryset()
        return Response({'data': self.get_serializer(qs, many=True).data})

    def retrieve(self, request, pk=None):
        return Response(data=self.get_serializer(self.get_object(pk)).data)

    def create(self, request):
        return Response({'action': 'create'})

    def update(self, request, pk=None):
        return Response({'action': 'update'})

    def partial_update(self, request, pk=None):
        return Response({'action': 'partial update'})

    def destroy(self, request, pk=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(data={'done': 'ok'}, status=HTTP_200_OK)


class MovieViewset(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieRateViewset(viewsets.ModelViewSet):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class ExampleViewset(viewsets.ReadOnlyModelViewSet):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_classes = {
        'rate': MovieRateSerializer,
        'default': MovieSerializer
    }
    permission_classes = [IsAuthenticatedOrReadOnlyCustom, ]
    authentication_classes = [TokenAuthentication, ]
    filterset_class = MovieFilterSet
    filter_backends = (filters.DjangoFilterBackend, )
    pagination_class = StandarResultsSetPagination

    def get_serializer_class(self):
        return self.serializer_classes[self.action] if self.action in self.serializer_classes.keys() else \
            self.serializer_classes['default']

    def get_serializer_context(self):
        context = super(MovieViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(methods=['POST'], detail=True)
    def rate(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=obj, user=request.user)

        return Response(data=self.get_serializer(serializer.instance).data)


class MovieRateViewSet(viewsets.ModelViewSet):
    queryset = MovieRate.objects.all()
    serializer_class = MovieRateSerializer
