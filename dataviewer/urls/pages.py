from django.conf.urls.defaults import *
urlpatterns = patterns('',
	url(r'new/?', 'dataviewer.views.pages.new', name='dataviewer.new_page'),
	url(r'create/?', 'dataviewer.views.pages.create', name='dataviewer.create_page'),
	url(r'edit/(?P<page_id>\d+)/?', 'dataviewer.views.pages.edit', name='dataviewer.edit_page'),
	url(r'update/(?P<page_id>\d+)/?', 'dataviewer.views.pages.update', name='dataviewer.update_page'),
	url(r'delete/(?P<page_id>\d+)/?', 'dataviewer.views.pages.delete', name='dataviewer.delete_page'),
	url(r'(?P<pagename>.+)/?', 'dataviewer.views.pages.view', name='dataviewer.view_page'),
	url(r'/?', 'dataviewer.views.pages.list', name='dataviewer.list_pages'),
)
