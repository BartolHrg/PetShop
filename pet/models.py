from typing import *;

from django.db import models;
try:
	from django.db.models import BaseManager;
except ImportError:
	BaseManager = dict;
pass
from django.http import QueryDict;

__all__ = ["Category", "Tag", "Pet", "PhotoUrl", "queryListInCNF", "querryPetRequest", ];

class Category(models.Model):
	class Meta: app_label = "pet";
	name: str = models.CharField(max_length = 32);
pass

class Tag(models.Model):
	class Meta: app_label = "pet";
	name: str = models.CharField(max_length = 32);
pass

statuses = ["available", "pending", "sold"];

class Pet(models.Model):
	class Meta: 
		app_label = "pet";
		constraints = [
			models.CheckConstraint(name="valid_status", check=models.Q(status__in=statuses)),
		];
	pass
	name: str = models.CharField(max_length = 32);
	category: Category = models.ForeignKey(Category, on_delete=models.CASCADE);
	photo_urls: list[str];
	tags = models.ManyToManyField(Tag);
	status: Literal["available"] | Literal["pending"] | Literal["sold"] = models.CharField(max_length = max(len(st) for st in statuses));
pass

class PhotoUrl(models.Model):
	class Meta: app_label = "pet";
	url: str = models.CharField(max_length = 32);
	pet: Pet = models.ForeignKey(Pet, on_delete=models.CASCADE);
pass

def queryListInCNF(query: BaseManager[Any], cnf: Iterable[Iterable[str]], transform: Callable[[str], dict[str, Any]]):
	"cnf example:"           "\n"
	"["                      "\n"
	"\t['+a', '+b', '-c'],"  "\n"
	"\t['+a', '+b', '-d'],"  "\n"
	"]"                      "\n"
	"means (a, b, and not c) or (a, b, and not d)"
	first = True;
	result: BaseManager = None;
	for ands in cnf:
		tmp = query;
		for e in ands:
			t = transform(e[1 : ]);
			if   e[0] == "+":
				tmp = tmp.filter(**t);
			elif e[0] == '-':
				tmp = tmp.exclude(**t);
			pass
		pass
		if first:
			first = False;
			result = tmp;
		else:
			result = result.union(tmp);
		pass
	pass
	if result is not None:
		return result;
	else:
		return query;
	pass
pass
def querryPetRequest(query: BaseManager[Pet], req_dict: QueryDict):
	if "id"        in req_dict: query = query.filter(id                = int(req_dict["id       "]));
	if "name"      in req_dict: query = query.filter(name__iexact      =     req_dict["name     "]);
	if "namestart" in req_dict: query = query.filter(name__istartswith =     req_dict["namestart"]);
	if "namehas"   in req_dict: query = query.filter(naem__icontains   =     req_dict["namehas  "]);
	if "nameend"   in req_dict: query = query.filter(name__iendswith   =     req_dict["nameend  "]);
	
	query = queryListInCNF(query, req_dict.getlist("tags"      , []), lambda x: {"tag__id"    : int(x)});
	query = queryListInCNF(query, req_dict.getlist("categories", []), lambda x: {"category_id": int(x)});
	
	return query;
pass

# if not list(Category.objects.all()):
# 	cA = Category.objects.create(name="cA");
# 	cB = Category.objects.create(name="cB");
# 	cC = Category.objects.create(name="cC");
# pass
# if not list(Tag.objects.all()):
# 	tA = Tag.objects.create(name="tA");
# 	tB = Tag.objects.create(name="tB");
# 	tC = Tag.objects.create(name="tC");
# pass
# if not list(Pet.objects.all()):
# 	Pet.objects.create(name="pA", category_id=cB.id, tags=[tA, tC]);
# 	Pet.objects.create(name="pB", category_id=cC.id, tags=[tB, tA]);
# pass
