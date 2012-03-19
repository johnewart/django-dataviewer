from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context, loader
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Context, loader
from django.db import models

from dataviewer.models import * 
from dataviewer.decorators import *

import pprint
import re

from django.conf import settings

try:
	print "Importing apps"
	for app in settings.DATAVIEWER_APPS:
		print "Importing %s" % (app)
		models = "%s.models" % (app)
		module = __import__(models, globals(), locals(), ["*"])
		for k in dir(module):
			locals()[k] = getattr(module, k)
except:
	print "Unable to import any apps' models"

def list(request):
    tables = ViewTable.objects.all()
    
    t = loader.get_template('dataviewer/tables/list.html')
    c = RequestContext(request,{ "tables": tables })
    return HttpResponse(t.render(c))

def new(request):
    available_models = models.get_models()
    model_list = []
    for model in available_models:
        m = re.match(r"<class '(.*?)'>", "%s" % (model))
        klass = m.group(1)
        name = klass.split(".")[-1]
        model_list.append({'name' : name, 'class': klass})

    t = loader.get_template('dataviewer/tables/new.html')   
    c = RequestContext(request,{ "available_models": model_list })
    return HttpResponse(t.render(c))
    
def create(request):
    table = ViewTable()
    if request.GET.has_key("model_name"):
        table.model = request.GET["model_name"]
    table.save()
    return HttpResponseRedirect("/tables/edit/%d" % (table.id))

def update(request, table_id):
    if request.POST:
        keys = request.POST.keys()
        for key in keys:
            if key.startswith("viewfield_"):
                print "KEY: %s" % (key)
                (junk,field_id) = key.split("_")
                field = ViewField.objects.get(pk = field_id)
                field.name = request.POST[key]
                print "Field name: %s" % (field.name)
                field.save()
                
        table = ViewTable.objects.get(pk = table_id)
        table.name = request.POST["name"]
        fields = request.POST.getlist("fields")
        functions = request.POST.getlist("functions")
        
        for field in fields:
            vf = ViewField()
            vf.name = field
            vf.field = field
            vf.save()
            table.fields.add(vf)
    
    
        for function in functions:
            vf = ViewField()
            vf.name = function
            vf.field = function
            vf.save()
            table.fields.add(vf)
            
        table.save()
        
    return HttpResponseRedirect("/tables/")

def remove_field(request):
    try:
        table_id = request.GET.get("table_id", request.GET.get("TABLE_ID"))
        viewfield_id = request.GET.get("viewfield_id", request.GET.get("VIEWFIELD_ID"))
        table = ViewTable.objects.get(pk = table_id)
        viewfield = ViewField.objects.get(pk = viewfield_id)
        table.fields.remove(viewfield)
        return HttpResponse(status=200)
    except:
        raise
        return HttpResponse(status=500)

def view(request, table_id):
    available_models = models.get_models()
    model_list = []
    for model in available_models:
        m = re.match(r"<class '(.*?)'>", "%s" % (model))
        klass = m.group(1)
        name = klass.split(".")[-1]
        model_list.append({'name' : name, 'class': klass})

    t = loader.get_template('dataviewer/manages.html')
    c = RequestContext(request,{ "available_models": model_list })
    return HttpResponse(t.render(c))

def edit(request, table_id):
    table = ViewTable.objects.get(pk = table_id)
    
    # Introspect the model 
    model_name = table.model

    package = ".".join(model_name.split(".")[0:-2])
    modelname = model_name.split(".")[-1]
    model = models.get_model(package, modelname)

    print "Model: (%s) %s <--> %s" % (package, model_name,model)

    existing_fields = []
    fields = []
    functions = []
    mtom_fields = {}
    
    for field in table.fields.all():
        existing_fields.append(field.field)
        
    if model: 
        for field in model._meta.fields:
            try:
                i = existing_fields.index(field.attname)
            except ValueError:
                fields.append(field.attname)
            
        for mtom in model._meta.many_to_many:
            m = re.match(r"<class '(.*?)'>", "%s" % (mtom.rel.to))
            klass = m.group(1)
            mtom_fields[mtom.name] = ViewTable.objects.filter(model=klass).all()
        
        import pprint
        pprint.pprint(mtom_fields)
        all_funcs = dir(model)
    
        for function_name in all_funcs:
            if not function_name.startswith("_"):
                try: 
                    i = existing_fields.index(function_name)
                except ValueError:
                    functions.append(function_name)

        fields.sort()
        functions.sort()

    ctxt = { 
        "table": table, 
        'available_fields' : fields, 
        'mtom_fields' : mtom_fields, 
        'functions' : functions 
    }
                
    t = loader.get_template('dataviewer/tables/edit.html')
    c = RequestContext(request, ctxt)
    return HttpResponse(t.render(c))

def delete(request, table_id):
    table = ViewTable.objects.get(pk = table_id)
    table.delete()
    return HttpResponseRedirect("/tables/")

