
from rest_framework import viewsets, permissions;

from pet.models import *;
from pet.serializers import *;

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all();
	serializer_class = CategorySerializer;
	permission_classes = [permissions.AllowAny];
pass

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all();
	serializer_class = TagSerializer;
	permission_classes = [permissions.AllowAny];
pass

class PetViewSet(viewsets.ModelViewSet):
	queryset = Pet.objects.all();
	serializer_class = PetSerializer;
	permission_classes = [permissions.AllowAny];
pass

class PhotoUrlViewSet(viewsets.ModelViewSet):
	queryset = PhotoUrl.objects.all();
	serializer_class = PhotoUrlSerializer;
	permission_classes = [permissions.AllowAny];
pass
