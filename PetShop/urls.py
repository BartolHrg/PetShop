"""PetShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include;

import pet.views;
import api.urls;

urlpatterns = [
	path('admin/', admin.site.urls),
	
	path("pet", pet.views.Pet.as_view()),
	# path("pet/update", pet.views.petUpdate),
	path("pet/<int:id>", pet.views.PetById.as_view()),
	
	path("tag", pet.views.Tag.as_view()),
	path("tag/<int:id>", pet.views.TagById.as_view()),
	
	path("category", pet.views.Category.as_view()),
	path("category/<int:id>", pet.views.CategoryById.as_view()),
	
	path("api/", include(api.urls)),
]

# {
#     a = await fetch("http://127.0.0.1:8000/api/tags/");
#     js = await a.json();
# }
# (4) [{…}, {…}, {…}, {…}]
# {
#     a = await fetch("http://127.0.0.1:8000/api/pets/");
#     js = await a.json();
# }
# VM1305:2          GET http://127.0.0.1:8000/api/pets/ 500 (Internal Server Error)
# (anonymous) @ VM1305:2
# Uncaught SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
# {
#     a = await fetch("http://127.0.0.1:8000/api/pets/");
#     js = await a.json();
# }
# VM1310:2          GET http://127.0.0.1:8000/api/pets/ 500 (Internal Server Error)
# (anonymous) @ VM1310:2
# Uncaught SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
# {
#     a = await fetch("http://127.0.0.1:8000/api/pets/");
#     js = await a.json();
# }

# b = await fetch("http://127.0.0.1:8000/api/tags/", { headers: {
#       'Accept': 'application/json',
#       'Content-Type': 'application/json'
#     },method: "POST", body: JSON.stringify({name: "tD"}) });