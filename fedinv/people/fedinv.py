from swag.models import Person 

# FIXME: use Django's auth system
def get_current_user():
	return Person.objects.get(id=0)
	
