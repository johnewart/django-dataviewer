import logging

from functools import update_wrapper, wraps
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404

from dataviewer.permissions import * 
from dataviewer.models import * 

def require_page_groups(view_func):
	"""	
		 Check to see if the current session user has permission to view this 
		 page. This is determined by getting the user from the active request
		 object, and the active page name in question. Then we get all the groups
		 from the page object and flatten them to an array for easy comparison. 
		 
		 If the user has no groups, we assume they are an Administrator currently
		 (this should be fixed). 
		 
		 We compare the groups that the user is in to the groups allowed to view 
		 the page, and if there's a match, we grant access, otherwise, send an 
		 HTTP 302-redirect to the unauthorized access URL.
	"""
	login_url = settings.LOGIN_URL
	unauthorized_url = settings.UNAUTHORIZED_URL
	
	def _wrapped_view(request, *args, **kwargs):
		"""
		Wrapper for the permission checking (this is where the actual work is done)
		"""
		#kwargs.update({'debug': True}) # Edit the keyword arguments -- here, enable debug mode no matter what
		pagename = kwargs["pagename"]
		p = Page.objects.get(name=pagename)
		user = request.user
		if not permitted_to_view_page(p, user):
			return HttpResponseRedirect('%s' % unauthorized_url)
		return view_func(request, *args, **kwargs)

	return wraps(view_func)(_wrapped_view)
