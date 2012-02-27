from django import template

import logging
import re 
import HTML 

from dataviewer.models import *
from dataviewer.permissions import * 

register = template.Library()

@register.inclusion_tag('blocks/page_tabs.html', takes_context=True)
def page_tabs(context):
	"""
	List all pages who are associated with the model currently registered in the 
	session variable 'dataviewer_model_name'. Only returns those pages which are 
	visible to the currently logged in user.  
	"""
	try:
		request = context['request']
		user = context["user"]
		model_name = request.session["dataviewer_model_name"]
	
		pages = Page.objects.filter(model = model_name)

		accessible = []
		
		for page in pages:
			if permitted_to_view_page(page, user):
				accessible.append(page)
			
		return {
		 'pages': accessible
		}
	except Exception:
		return {}
		
@register.inclusion_tag('blocks/model_field_select.html', takes_context=True) 
def model_field_select(context, model_name, selected_field = None):
	"""
	Generate a list of model fields available, as well as specify which one is selected
	"""
	package = ".".join(model_name.split(".")[1:-2])
	modelname = model_name.split(".")[-1]
	model = models.get_model(package, modelname)
	fields = []

	for field in model._meta.fields:
		fields.append(field.attname)

	return {
		'fields' : fields, 
		'selected_field' : selected_field
	}

	