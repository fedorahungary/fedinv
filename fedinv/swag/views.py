from django.http import HttpResponse
from django.template import RequestContext, loader
from django.template.defaulttags import register
from django.core.mail import send_mail

from fedinv import settings
from people.fedinv import get_current_user
from swag.models import SwagType, Person, swag_id_to_name
from swag.forms import OrderForm

@register.filter
def person_swag_amount(p, swag_id):
	if swag_id in p.d_held_swag:
		return p.d_held_swag[swag_id]
	return "0"

def index(request):
	t = loader.get_template('swag/index.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
	})
	return HttpResponse(t.render(c))

def manage_swag(request):
	t = loader.get_template('swag/all.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'swag_list': SwagType.objects.all(),
	})
	return HttpResponse(t.render(c))

def manage_people(request):
	t = loader.get_template('swag/manage-people.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'ppl_list': Person.objects.all(),
	})
	return HttpResponse(t.render(c))

def edit_person(request, person_id):
	t = loader.get_template('swag/edit-person.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'person': Person.objects.get(id = int(person_id)),
	})
	return HttpResponse(t.render(c))

def order(request, person_id, swag_id):
	t = loader.get_template('swag/order.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'person': Person.objects.get(id = int(person_id)),
		'swag': SwagType.objects.get(id = int(swag_id)),
		'form': OrderForm(),
	})
	return HttpResponse(t.render(c))

def confirmed_order(request, person_id, swag_id):
	me = get_current_user()
	if request.method == 'GET':
		form = OrderForm()
	else:
		form = OrderForm(request.POST)
		if form.is_valid():
			p = Person.objects.get(id = int(person_id))
			amount = form.cleaned_data['amount']
			if (p.has_swag(swag_id, amount)):
				if settings.FEDINV_SEND_EMAILS == True:
					# Send the order to the person
					body = settings.FEDINV_ORDER_BODY %{
						"to": p.name,
						"from": me.name,
						"amount": amount,
						"swag": swag_id_to_name(swag_id)}
					send_mail(settings.FEDINV_ORDER_SUBJECT % {"from": me.name},
					body, settings.FEDINV_EMAIL_FROM, [p.email])
					# Send confirmation to the buyer
					body = settings.FEDINV_ORDER_CONFIRMATION_BODY %{
						"to":  me.name,
						"from": p.name,
						"amount": amount,
						"swag": swag_id_to_name(swag_id)}
					send_mail(settings.FEDINV_ORDER_CONFIRMATION_SUBJECT %{
						"from": p.name}, body, settings.FEDINV_EMAIL_FROM,
						[me.email])
				return HttpResponse("You want %d of swag" % amount)
			else:
				return HttpResponse("%s hasn't got enough of that!" % p.name)
		else:
			return HttpResponse("ERROR: invalid data")
	return HttpResponse("ERROR: POST required!")

def edit_swag(request, swag_id):
	# Find ambassadors who have $swag_id
	plist = []
	for p in Person.objects.all():
		if (swag_id in p.d_held_swag):
			plist.append(p)

	t = loader.get_template('swag/edit-swag.html')
	c = RequestContext(request, {
		'region': settings.FEDINV_REGION,
		'swag_id': swag_id,
		'plist': plist,
	})
	return HttpResponse(t.render(c))
