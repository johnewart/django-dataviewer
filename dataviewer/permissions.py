import logging
from dataviewer.models import * 

def permitted_to_view_page(page, user):
	"""	
	Check to see if the user specified is able to view the page specified. This is primarily used by the 
	template tag for displaying a particular page as well as for generating the list of pages
	a user is allowed to view (so as to be able to hide any non-viewable pages)
	"""
	page_groups = map(lambda x: x.name, page.groups.all())
	try:
		user_groups = user.ldap_user._get_groups().get_group_names()
	except Exception:
		logging.debug("Unable to lookup LDAP data, defaulting to administrative user")
		user_groups = ['Administrators']
		
	for group in user_groups:
		logging.debug("Considering: %s vs %s", group, page_groups)
		if group in page_groups:
			logging.debug("Permission granted!")
			return True
	
	logging.debug("No access!")
	return False
			
