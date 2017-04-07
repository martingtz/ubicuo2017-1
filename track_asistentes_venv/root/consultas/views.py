from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from json_rest.models import Consejeros
from django.contrib.auth.decorators import login_required
##E20051860107019126600B75
# Create your views here.
@login_required
def consulta_form(request):
	rfid = ""
	if request.method == 'GET':
		return render(request,'consultas_template/consultas.html')
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
	        #returing the template 
			return render(request,'consultas_template/consultas.html',context)
		except KeyError:
	    	   return HttpResponse("LLave No valida en el post")
	   	except ObjectDoesNotExist,DoesNotExist:
			return HttpResponse("No hay ningun asistente asociado al RFID")

	return render(request,'consultas_template/consultas.html')