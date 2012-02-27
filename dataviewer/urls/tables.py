from django.conf.urls.defaults import *
urlpatterns = patterns('',
	url(r'new/?', 'dataviewer.views.tables.new', name='dataviewer.new_table'),
	url(r'create/?', 'dataviewer.views.tables.create', name='dataviewer.create_table'),
	url(r'edit/(?P<table_id>\d+)/?', 'dataviewer.views.tables.edit', name='dataviewer.edit_table'),
	url(r'update/(?P<table_id>\d+)/?', 'dataviewer.views.tables.update', name='dataviewer.update_table'),
	url(r'delete/(?P<table_id>\d+)/?', 'dataviewer.views.tables.delete', name='dataviewer.delete_table'),
	url(r'(?P<table_id>\d+)/?', 'dataviewer.views.tables.view', name='dataviewer.view_table'),
	url(r'/?', 'dataviewer.views.tables.list', name='dataviewer.list_tables'),
)
