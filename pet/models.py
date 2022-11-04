from __future__ import annotations
from dataclasses import dataclass
import re;
from typing import *;

from django.db import models;
try:
	from django.db.models import BaseManager;
except ImportError:
	BaseManager = dict;
pass
from django.http import QueryDict;

__all__ = ["Category", "Tag", "Pet", "PhotoUrl", "queryListInCNF", "querryPetRequest", ];

def toJson(obj) -> Any:
	if   isinstance(obj, BaseJsoner):
		return obj.toJson();
	elif isinstance(obj, list):
		return [toJson(el) for el in obj];
	elif isinstance(obj, dict):
		return { key: toJson(value) for (key, value) in obj.items() };
	else:
		return obj;
	pass
pass
class BaseJsoner:
	def toJson(self) -> Any:
		json = {};
		for name in self.__annotations__.keys():
			attr = getattr(self, name);
			json[name] = toJson(attr);
		pass
		return json;
	pass
	@classmethod
	def fromJson(cls, json: dict):
		return cls(**json);
	pass
pass

class Category(models.Model):
	class Meta: app_label = "pet";
	name: str = models.CharField(max_length = 32);
	
	def toJsoner(self) -> Category.Jsoner:
		return self.Jsoner.fromModel(self);
	pass
	@dataclass
	class Jsoner(BaseJsoner):
		id: int;
		name: str;
		
		@classmethod
		def fromModel(cls, category: Category) -> Category.Jsoner:
			return cls(category.id, category.name);
		pass
		@classmethod
		def toModel(self) -> Category:
			if hasattr(self, "id"):
				try: 
					obj = Category.objects.get(id=self.id);
				except models.Model.DoesNotExist:
					return Category(id=self.id, name=self.name);
				else:
					return obj;
				pass
			else:
				return Category(name=self.name);
			pass
		pass
	pass
pass

class Tag(models.Model):
	class Meta: app_label = "pet";
	name: str = models.CharField(max_length = 32);
	
	def toJsoner(self) -> Tag.Jsoner:
		return self.Jsoner.fromModel(self);
	pass
	@dataclass
	class Jsoner(BaseJsoner):
		id: int;
		name: str;
		
		@classmethod
		def fromModel(cls, tag: Tag) -> Tag.Jsoner:
			return cls(tag.id, tag.name);
		pass
		@classmethod
		def toModel(self) -> Tag:
			if hasattr(self, "id"):
				try: 
					obj = Tag.objects.get(id=self.id);
				except models.Model.DoesNotExist:
					return Tag(id=self.id, name=self.name);
				else:
					return obj;
				pass
			else:
				return Tag(name=self.name);
			pass
		pass
	pass
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
	status: Literal["available"] | Literal["pending"] | Literal["sold"] = models.CharField(max_length = max(len(st) for st in statuses));
	tags = models.ManyToManyField(Tag);
	
	def toJsoner(self) -> Pet.Jsoner:
		return self.Jsoner.fromModel(self);
	pass
	@dataclass
	class Jsoner(BaseJsoner):
		id: int | None;
		name: str;
		category: Category.Jsoner;
		status: Literal["available"] | Literal["pending"] | Literal["sold"];
		tags: list[Tag.Jsoner];
		photo_urls: list[PhotoUrl.Jsoner];
		
		@classmethod
		def fromModel(cls, pet: Pet) -> Pet.Jsoner:
			return cls(
				id=pet.id if hasattr(pet, "id") else None,
				name=pet.name,
				category=Category.Jsoner.fromModel(pet.category),
				status=pet.status,
				tags=[Tag.Jsoner.fromModel(tag) for tag in pet.tags.all()],
				photo_urls=[PhotoUrl.Jsoner.fromModel(photo_url) for photo_url in PhotoUrl.objects.filter(pet__id=pet.id)],
			);
		pass
		@classmethod
		def toModel(self) -> Pet:
			category = self.category.toModel();
			assert isinstance(self.status, self.__annotations__["status"]);
			_tags_tmp = {tag.id: tag.name for tag in self.tags};
			tags = list(Tag.objects.filter(id__in=_tags_tmp.keys()));
			assert len(_tags_tmp) == len(tags) and all(_tags_tmp[tag.id] == tag.name for tag in tags);
			if hasattr(self, "id"):
				try:
					obj = Pet.objects.get(id=self.id);
				except models.Model.DoesNotExist:
					obj = Pet(id=self.id, name=self.name, category=category, status=self.status);
				pass
				obj.tags.set(tags);
				return obj;
			else:
				obj = Pet(name=self.name, category=category, status=self.status);
				obj.tags.set(tags);
				return obj;
			pass
		pass
	pass
pass

class PhotoUrl(models.Model):
	class Meta: app_label = "pet";
	url: str = models.CharField(max_length = 32);
	pet: Pet = models.ForeignKey(Pet, on_delete=models.CASCADE);

	def toJsoner(self) -> PhotoUrl.Jsoner:
		return self.Jsoner.fromModel(self);
	pass
	@dataclass
	class Jsoner(BaseJsoner):
		id: int;
		url: str;
		pet_id: int;
		
		@classmethod
		def fromModel(cls, photo_url: PhotoUrl) -> PhotoUrl.Jsoner:
			return cls(photo_url.id, photo_url.url, photo_url.pet.id);
		pass
		@classmethod
		def toModel(self) -> PhotoUrl:
			try:
				pet = Pet.objects.get(id=self.pet_id);
			except models.Model.DoesNotExist:
				raise;
			pass
			if hasattr(self, "id"):
				try:
					obj = PhotoUrl.objects.get(id=self.id);
				except models.Model.DoesNotExist:
					return PhotoUrl(id=self.id, url=self.url, pet=pet);
				else:
					return obj;
				pass
			else:
				return PhotoUrl(url=self.url, pet=pet);
			pass
		pass
	pass
pass

def queryListInCNF(query: BaseManager[Any], cnf: list[str], transform: Callable[[str], dict[str, Any]]):
	"cnf example:"           "\n"
	"x=i23i25x78&x=i23e25x79"    "\n"
	"means (23, 25, and not 78) or (23, not 25, and not 79)"
	# cnf: Iterable[Iterable[str]]
	
	first = True;
	result: BaseManager = None;
	for ands in cnf:
		tmp = query;
		for e in re.finditer(r"(i|x)(\d+)", ands):
			op = e.group(1);
			t = transform(e.group(2));
			if   op == "i":
				tmp = tmp.filter(**t);
			elif op == 'x':
				tmp = tmp.exclude(**t);
			pass
			print(list(tmp));
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
	
	# tmp = parseCnfList(req_dict.get("categories", "[]"), lambda x: x);
	# query = queryListInCNF(query, parseCnfList(req_dict.get("tags"      , "[]"), lambda x: x), lambda x: {"tag__id"    : int(x)});
	# query = queryListInCNF(query, tmp, lambda x: {"category_id": int(x)});
	
	query = queryListInCNF(query, req_dict.getlist("tags"      , []), lambda x: {"tags__id"    : int(x)});
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
