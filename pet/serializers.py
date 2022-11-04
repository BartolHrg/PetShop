
from rest_framework import serializers;
from .models import *;

class CategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Category;
		fields = ["id", "name"];
	pass
pass

class TagSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tag;
		fields = ["id", "name"];
	pass
pass

class PetSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Pet;
		fields = ["id", "name", "category", "tags", "status"]; # "photo_url__url", # for some reason, it doesn't work
	pass
pass

class PhotoUrlSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = PhotoUrl;
		fields = ["id", "url"];
	pass
pass


