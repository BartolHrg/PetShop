from typing import *;

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect;
from django.shortcuts import render;
from django.views import View;

from pet import models
from pet.forms import *;

def renderFromRequest(request: HttpRequest, prev_form=None) -> HttpResponse:
	form = prev_form;
	tags = [tag.toJsoner() for tag in models.Tag.objects.all()];
	categories = [category.toJsoner() for category in models.Category.objects.all()];
	pets = models.querryPetRequest(models.Pet.objects.all(), request.GET);
	ptelsl = [pet.toJsoner() for pet in pets];
	# print("\t\t", ptelsl);
	if form is None: form = NewPetForm();
	individual_forms = {pet.id: PetForm.fromModel(pet) for pet in pets};
	retur = render(request, "./pet_list.html", {
		"pets": ptelsl, 
		"tags":tags, 
		"categories":categories, 
		"new_pet_form": form, 
		"individual_forms": individual_forms
	});
	return retur;
pass
class Pet(View):
	def get(self, request: HttpRequest, prev_form=None) -> HttpResponse:
		return renderFromRequest(request, prev_form);
	pass
	def post(self, request: HttpRequest) -> HttpResponse:
		form = PetForm(request.POST);
		print(request.POST);
		if form.is_valid():
			cat = models.Category.objects.get(id=int(form.cleaned_data["category"]));
			new_pet = models.Pet.objects.create(name=form.cleaned_data["name"], category=cat, status="available");
			tags = [int(id) for id in form.cleaned_data["tags"]];
			# print(tags);
			new_pet.tags.set(models.Tag.objects.filter(id__in=tags));
			form = None;
		else:
			print("Wrong form");
			print(form.errors);
			print(form.non_field_errors());
			print(dict(form.errors));
		pass
		return HttpResponseRedirect(request.POST.get("location"));
		return renderFromRequest(request, form);
	pass
pass
# def petUpdate(request: HttpRequest) -> HttpResponse:
# 	if request.method == "POST":
# 		form = PetForm(request.POST);
# 		if not form.is_valid(): raise Exception;
		
# 		id = request.POST.get("id", None);
# 		if id is None: raise Exception;
# 		try:
# 			pet = models.Pet.objects.get(id=id);
# 		except models.Pet.DoesNotExist:
# 			raise;
# 		pass
# 		pet.name        =      form.cleaned_data["name"];
# 		pet.category_id =      int(form.cleaned_data["category"]);
# 		pet.status      =     models.statuses[int(form.cleaned_data["status"])];
# 		pet.save();

# 		tags = [int(id) for id in form.cleaned_data["tags"]];
# 		pet.tags.set(models.Tag.objects.filter(id__in=tags));
		
# 		return renderFromRequest(request);
# 	else:
# 		raise Exception;
# 	pass
# pass

class PetById(View):
	def delete(self, request: HttpRequest, id: int) -> HttpResponse:
		pet = models.Pet.objects.get(id=id);
		pet.delete();
		return renderFromRequest(request);
	pass
	
	def post(self, request: HttpRequest, id: int) -> HttpResponse:
		form = PetForm(request.POST);
		if not form.is_valid(): raise Exception;
		
		id = request.POST.get("id", None);
		if id is None: raise Exception;
		try:
			pet = models.Pet.objects.get(id=id);
		except models.Pet.DoesNotExist:
			raise;
		pass
		pet.name        =      form.cleaned_data["name"];
		pet.category_id =      int(form.cleaned_data["category"]);
		pet.status      =     models.statuses[int(form.cleaned_data["status"])];
		pet.save();

		tags = [int(id) for id in form.cleaned_data["tags"]];
		pet.tags.set(models.Tag.objects.filter(id__in=tags));
		
		return HttpResponseRedirect(request.POST.get("location"));
		return renderFromRequest(request);
	pass
pass
