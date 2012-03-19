
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import admin

class ViewField(models.Model):
	name = models.CharField(max_length=200)
	field = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name

class ViewTable(models.Model):
	"Table is a model that represents a table of data that maps to a model and certain fields"
	name = models.CharField(max_length=200)
	model = models.CharField(max_length=200)
	fields = models.ManyToManyField(ViewField)
	embedded_tables = models.ManyToManyField('self')
	
	def __str__(self):
		return self.name

class Page(models.Model):
	"Viewable page we can use to create custom groupings of data"
	name = models.SlugField(unique=True,help_text="Automatically derived from the title, this is what becomes the URL (i.e /tabs/[[name]])")
	title = models.CharField(max_length=200)
	model = models.CharField(max_length=200)
	body = models.TextField('Entry body as HTML', editable=True, blank=True, null=True)
	groups = models.ManyToManyField(Group)
	tables = models.ManyToManyField(ViewTable)
	mtom_mappings = models.TextField()
	
	def __str__(self):
		return self.title
