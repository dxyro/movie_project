from django.urls import path
from rest_framework.routers import SimpleRouter

from movie_app.api.viewsets import MovieViewset, MovieRateViewset, ExampleViewset, MovieViewSet, MovieRateViewSet

router = SimpleRouter()
router.register('movie', MovieViewSet)
router.register('movierate', MovieRateViewSet)

urlpatterns = router.urls