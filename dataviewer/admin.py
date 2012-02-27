from django.contrib import admin
from dataviewer.models import *

class PageAdmin(admin.ModelAdmin):
  prepopulated_fields = {"name": ("title",)}
  fields = ("title", "name", "body", "groups", "tables")

class ViewTableAdmin(admin.ModelAdmin):
	pass

class GenericAdmin(admin.ModelAdmin):
	pass

admin.site.register(Page, PageAdmin)
admin.site.register(ViewTable, ViewTableAdmin)
