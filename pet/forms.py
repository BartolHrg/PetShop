

from django import forms
from pet import models

from pet.models import Category, Pet, Tag;


class NewPetForm(forms.Form):
	id       = forms.IntegerField(required=False, widget=forms.HiddenInput);
	name     = forms.CharField(label="name", max_length=32, required=True);
	# category = forms.IntegerField(required=False, label = "category id");
	category = forms.ChoiceField(label="category", choices=[], required=True);
	tags     = forms.MultipleChoiceField(label="tags", choices=[], widget=forms.CheckboxSelectMultiple(), required=False);
	
	def __init__(self, *args, tag_choices=None, category_choices=None, **kwargs):
		super().__init__(*args, **kwargs);
		if tag_choices is None:
			tag_choices = [(tag.id, tag.name) for tag in Tag.objects.all()];
		pass
		if category_choices is None:
			category_choices = [(category.id, category.name) for category in Category.objects.all()];
		pass
		self.fields['tags'    ].choices =      tag_choices;
		self.fields['category'].choices = category_choices;
	pass
pass

class PetForm(NewPetForm):
	status = forms.ChoiceField(label="status", choices=enumerate(models.statuses), required=True);
	
	@classmethod
	def fromModel(cls, model: Pet) -> "PetForm":
		form = cls();
		# print("here");
		form.fields["id"       ].initial = model.id;
		form.fields["name"     ].initial = model.name;
		form.fields["category" ].initial = (model.category.id, model.category.name);
		form.fields["tags"     ].initial = [(tag.id, tag.name) for tag in model.tags.all()];
		form.fields["status"   ].initial = (models.statuses.index(model.status), model.status);
		# print();
		# print('x');
		# print(form);
		# print('y');
		return form;
	pass
pass

class TagForm(forms.ModelForm):
	class Meta:
		model = Tag;
		fields = ["id", "name"];
	pass
pass

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category;
		fields = ["id", "name"];
	pass
pass
