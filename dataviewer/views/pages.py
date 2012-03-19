from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, Template, Context, loader
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.template.defaultfilters import slugify

import django.contrib.auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Context, loader
from django.db import models

from dataviewer.models import * 
from dataviewer.decorators import *
from dataviewer.utils import Table

import datetime
import HTML
import html_table
import pprint
import re 

from django.conf import settings

try:
    for app in settings.DATAVIEWER_APPS:
        models = "%s.models" % (app)
        module = __import__(models, globals(), locals(), ["*"])
        for k in dir(module):
            locals()[k] = getattr(module, k)
except:
    print "Unable to import any apps' models"

def create(request):
    if request.POST:
        page = Page()
        page.title = request.POST["title"]
        page.name = slugify(request.POST["title"])
        page.model = request.POST['model']
        page.save()
        return HttpResponseRedirect("/pages/edit/%d" % (page.id))

def new(request):
    """
    Create a page

    :param request: Django request object
    """
    available_models = models.get_models()
    model_list = []
    for model in available_models:
        m = re.match(r"<class '(.*?)'>", "%s" % (model))
        klass = m.group(1)
        name = klass.split(".")[-1]
        model_list.append({'name' : name, 'class': klass})

    t = loader.get_template('dataviewer/pages/new.html')
    c = RequestContext(request,{ "available_models": model_list })
    return HttpResponse(t.render(c))

def edit(request, page_id):
    """
    Edit a page

    :param request: Django request object
    :param page_id: PK ID of the page to be edited
    """
    page = Page.objects.get(pk = page_id)
    groups = Group.objects.all()
    tables = ViewTable.objects.filter(model = page.model)

    # Introspect the model
    model_name = page.model

    package = ".".join(model_name.split(".")[1:-2])
    modelname = model_name.split(".")[-1]
    model = models.get_model(package, modelname)

    print "Model: %s <--> %s" % (model_name,model)

    mtom_fields = {}

    if model:
        for mtom in model._meta.many_to_many:
            m = re.match(r"<class '(.*?)'>", "%s" % (mtom.rel.to))
            klass = m.group(1)
            mtom_fields[mtom.name] = ViewTable.objects.filter(model=klass).all()

    ctxt = {
        'page' : page,
        'groups' : groups,
        'tables' : tables,
        'mtom_fields' : mtom_fields,
    }

    return render_to_response('dataviewer/pages/edit.html', ctxt, context_instance=RequestContext(request))

def update(request, page_id):
    """
    Update a page

    :param request: Django request object
    :param page_id: PK ID of the page to be updated
    """
    page = Page.objects.get(pk = page_id)
    page.title = request.POST["title"]
    page.name = request.POST["name"]
    groups = request.POST.getlist("groups")
    tables = request.POST.getlist("tables")

    m2m_mappings = {}

    for key in request.POST:
        if key.endswith("_m2mtable"):
            field = key.split("_")[0]
            m2m_mappings[field] = request.POST[key]

    for group_id in groups:
        group = Group.objects.get(pk = group_id)
        page.groups.add(group)

    for table_id in tables:
        table = ViewTable.objects.get(pk = table_id)
        page.tables.add(table)

    import json
    page.mtom_mappings = json.dumps(m2m_mappings)
    page.save()
    return HttpResponseRedirect("/pages/edit/%d" % (page.id))


def delete(request, page_id):
    """
    Delete a page

    :param request: Django request object
    :param page_id: PK ID of the page to be deleted
    """
    page = Page.objects.get(pk = page_id)
    page.delete()
    return HttpResponseRedirect("/pages/")

def list(request):
    """
    List all pages

    :param request: Django request object
    """
    pages = Page.objects.all().order_by('model')
    ctxt = {
        'pages' : pages
    }
    return render_to_response('dataviewer/pages/list.html', ctxt, context_instance=RequestContext(request))

@login_required
@require_page_groups
def view(request, pagename):
    """
    This is the page-view function that loads up the template from the
    database (this makes it user-editable) and wraps it in a string
    which we prefix by loading the dataviewer_tags tag library
    (located in the templatetags directory). This string is then evaluated
    by Django's template rendering engine to produce the actual output.

    Users can, because of this method, create custom page views with whatever
    data they want from the currently viewed case.

    This function requires :py:func:`dataviewer.decorators.require_page_groups` to not redirect you

    :param request: Django request object
    :param pagename: The short name of the page to view, passed in via URL
    """
    page = Page.objects.get(name=pagename)

    ctx = Context()

    tmplbody = "{% load dataviewer_tags %}\n" + str(page.body)
    template = loader.get_template_from_string(tmplbody)


    pk_id = request.session["dataviewer_pk_id"]
    model_name = request.session["dataviewer_model_name"]

    package = ".".join(model_name.split(".")[0:-2])
    modelname = model_name.split(".")[-1]

    print "Model name: %s (%d)" % (model_name, int(pk_id))
    __import__(package)

    model = eval(modelname)

    wanted = model.objects.get(pk = pk_id)

    print "Found: %s" % (wanted)

    body = template.render(ctx).encode("utf8")
    tables = page.tables.all()
    tablehtml = ""
    table_list = []

    for table in tables:
        result = {}
        properties = []
        for field in table.fields.all():
            print "Field: %s -> %s" % (field.name, field.field)
            fieldvalue = getattr(wanted, field.field)
            if callable(fieldvalue):
                data = fieldvalue()
            else:
                data = fieldvalue

            properties.append( (field.name, data)	 )

        generated = Table(table.name).generate(properties)
        result['html'] = generated[1]
        result['title'] = generated[0]
        table_list.append(result)

    if page.mtom_mappings:
        import json
        m2m_mappings = json.loads(page.mtom_mappings)

        for m2m_field in m2m_mappings:
            table_id = int(m2m_mappings[m2m_field])
            table = ViewTable.objects.get(pk = table_id)
            print "Loading table for %s using table %d " % (m2m_field,table_id)
            sub_objects = getattr(wanted, m2m_field)

            for sub_object in sub_objects.all():
                result = {}
                properties = []
                print "Result: %s" % (result)
                for field in table.fields.all():
                    print "Field: %s -> %s" % (field.name, field.field)
                    fieldvalue = getattr(sub_object, field.field)
                    if callable(fieldvalue):
                        data = fieldvalue()
                    else:
                        data = fieldvalue

                    properties.append( (field.name, data)	 )

                generated = Table("").generate(properties)
                result['html'] = generated[1]
                result['title'] = generated[0]
                table_list.append(result)

    ctxt = {
        'pagecontent': body,
        'tables' : table_list
    }
    return render_to_response('dataviewer/page.html', ctxt, context_instance=RequestContext(request))

