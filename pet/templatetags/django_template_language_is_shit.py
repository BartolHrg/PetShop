
import django.template;

register = django.template.Library();
@register.filter
def return_item(l, i):
	# print(l, type(l), i, type(i));
	# print(l[i], type(l[i]));
	try:
		return l[i]
	except:
		return None