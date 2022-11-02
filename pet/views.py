import json
from typing import *;
from django.http import HttpRequest, HttpResponse;
from django.shortcuts import render
from django.views import View

from pet import models;

class Pet(View):
	def get(self, request: HttpRequest) -> HttpResponse:
		pets = models.querryPetRequest(models.Pet.objects.all(), request.GET);
		ptelsl = [pet for pet in pets];
		for pet in ptelsl:
			pet.tagsl = list(pet.tags.all());
		pass
		# print("\t\t", ptelsl);
		return render(request, "./pet_list.html", {"pets": ptelsl});
	pass
	def post(self, request: HttpRequest) -> HttpResponse:
		models.Category.objects.all().delete();
		cA = models.Category.objects.create(name="cA");
		cB = models.Category.objects.create(name="cB");
		cC = models.Category.objects.create(name="cC");

		models.Tag.objects.all().delete();
		tA = models.Tag.objects.create(name="tA");
		tB = models.Tag.objects.create(name="tB");
		tC = models.Tag.objects.create(name="tC");
		
		models.Pet.objects.all().delete();
		pA = models.Pet.objects.create(name="pA", category_id=cB.id, status="available"); pA.tags.set([tA, tC]);
		pB = models.Pet.objects.create(name="pB", category_id=cC.id, status="sold"     ); pB.tags.set([tB, tA, tC]);
		
		# data = json.loads(request.body);
		# # {
		# # 	"name": "doggie",
		# # 	"category": {
		# # 		"id": 1,
		# # # 		"name": "Dogs"
		# # 	},
		# # 	"photoUrls": [
		# # 		"string"
		# # 	],
		# # 	"tags": [
		# # 		{
		# # 			"id": 0,
		# # # 			"name": "string"
		# # 		}
		# # 	],
		# # 	"status": "available"
		# # }
		# models.Pet.objects.create(
		# 	name=data["name"],
		# 	category=models.Category()
		# )
		...
		# return HttpResponse(status=200);
		return self.get(request);
	pass
pass


def petByIdGet(request: HttpRequest, id: int) -> HttpResponse:
	...
pass
def petByIdHead(request: HttpRequest, id: int) -> HttpResponse:
	...
pass
def petByIdPut(request: HttpRequest, id: int) -> HttpResponse:
	...
pass
def petByIdPost(request: HttpRequest, id: int) -> HttpResponse:
	...
pass
def petByIdDelete(request: HttpRequest, id: int) -> HttpResponse:
	...
pass
def petById(request: HttpRequest, id: int) -> HttpResponse:
	...
pass

