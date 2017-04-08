from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from consultas_app.models import Consejeros
from django.contrib.auth.decorators import login_required

from django.contrib import messages

##E20051860107019126600B75
# Create your views here.
@login_required
def consulta_form(request):
	rfid = ""
	context = ""
	if request.method == 'GET':
		return render(request,'consultas_app_templates/consultas.html')
	#if post request came 
	if request.method == 'POST':
		try:
	        #getting values from post
	 		rfid = request.POST.get('rfid')
			if rfid == "":
	        	 return HttpResponse("No hay rfid")	 

			consejero=Consejeros.objects.get(rfid=rfid)
	        #adding the values in a context variable 
			context = {
	            'id': consejero.id,
	            'nombre': consejero.nombre,
	            'facultad': consejero.facultad,
	            'cargo': consejero.cargo,
	            'suplente': consejero.suplente,
	            'image_path': consejero.image_path
	        }   
		except KeyError:
				messages.success(request, 'Error accediendo al POST request')
				pass
	   	except ObjectDoesNotExist,DoesNotExist:
	   		messages.success(request, 'No hay ningun asistente asociado al RFID')
	   		pass
	return render(request,'consultas_app_templates/consultas.html',context)