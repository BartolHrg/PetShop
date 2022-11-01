from typing import *;
from django.http import HttpRequest, HttpResponse;
from django.shortcuts import render
from django.views import View

from pet import models;

class Pet(View):
	def get(self, request: HttpRequest) -> HttpResponse:
		return render(request, "./pet_list.html", {"greeting": "ja sam Bartol Hrg"});
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

