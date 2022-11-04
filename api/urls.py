from django.urls import include, path
from rest_framework import routers
from . import views;

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet);
router.register(r'tags'      , views.     TagViewSet);
router.register(r'pets'      , views.     PetViewSet);
router.register(r'photos'    , views.PhotoUrlViewSet);

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
];
