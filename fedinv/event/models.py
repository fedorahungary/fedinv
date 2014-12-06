from django.db import models
from django.template.defaulttags import register
import json

from swag.models import swag_id_to_name
from swag.models import Person

# JSON format description for event data
# (A kernel developer loves specs...)
# 
# In the JSON there are multiple sections,
# each section has a specific meaning. If the
# implementation doesn't understand a specific
# section specifier, then it must IGNORE it.
# Otherwise, render it as they please.
# Currently, the following SectionSpecifiers are
# defined:
# SECTION_ITEM_USAGE -> 1
#     Describes how many items were used as part
#     of the event.
# SECTION_PRESENT_PEOPLE -> 2
#    A simple list of who was at the event
#

@register.filter
def parse_event_data_html(json_data):
	data = json.loads(json_data)
	html = ""
	for spec in data:
		val = data[spec]
		if spec == "1": # SECTION_ITEM_USAGE
			html += 'The following items were used:<br />'
			for item in val:
				html += "<ul>" + swag_id_to_name(int(item))
				html += " (" + str(val[item]) +") </ul>"
		elif spec == "2": # SECTION_PRESENT_PEOPLE
			html += 'The following ambassadors were present:<br />'
			for item in val:
				html += "<ul>" + Person.objects.get(id=int(item)).name
				html += "</ul>"
	return html
		

class InvEvent(models.Model):
	name = models.CharField(max_length=500)
	time_from = models.DateField()
	time_until = models.DateField()
	responsible = models.IntegerField()
	# Data for the event, who was there, what swag was used.. etc
	data = models.CharField(max_length=50000)

	def __unicode__(self):
		return self.name
