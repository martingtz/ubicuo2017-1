from django.shortcuts import render
import json
import base64
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
from alta.models import Consejeros
from alta.models import Rfid
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.contrib.auth.decorators import login_required
# Create your views here. E20051860107019126600B74
## Tag to login required to access this view
@login_required
def alta_form(request):
	## Check if is a POST request
	if request.method == "POST":
		## extensions admited for images
		image_ext =['jpg','png']
		try:
			## Check from what form comes the request
			if 'submit-form1' in request.POST:
				# Store all request POST fields in a dictionary
				dictionary_post_values = {}
				dictionary_post_values['rfid'] = request.POST.get('rfid');
				dictionary_post_values['id'] = request.POST.get('id');
				dictionary_post_values['nombre'] = request.POST.get('name');
				dictionary_post_values['facultad'] = request.POST.get('facultad');
				dictionary_post_values['cargo'] = request.POST.get('cargo');
				dictionary_post_values['suplente'] = request.POST.get('suplente');
				dictionary_post_values['image_path'] = request.FILES.get('imageToUpload');

				print dictionary_post_values
				## Validate if exists empty fields
				value_list = dictionary_post_values.values()
				for value in value_list:
					if value == '' or value is None:
						return HttpResponse("Hay campos vacios")
				## Save the image in object media file
				image_uploaded = request.FILES.get('imageToUpload');
				## Validate if the extension is "jpg" or "png"
				ext=image_uploaded.name.split('.')
				ext=ext[len(ext)-1]

				if ext not in image_ext:
					return HttpResponse("Tipo de imagen no admitido")
				## Get FileSystemStorage instance
				fs = FileSystemStorage()
				## Save the file in the media folder with id by name
				image_name = fs.save(dictionary_post_values['id']+"."+ext, image_uploaded)
				## Get path from file uploaded
				uploaded_image_url = fs.url(image_name)
				## Add path to dictionary of POST fields
				dictionary_post_values['image_path'] = "."+uploaded_image_url;
				## Save in bd
				is_suplente = True
				if dictionary_post_values['suplente'] == 'false':
					is_suplente = False

				## Save consejero created with the values of form in database 
				consejero=Consejeros(id =dictionary_post_values['id'], nombre =dictionary_post_values['nombre'],facultad=dictionary_post_values['facultad'],cargo=dictionary_post_values['cargo'],image_path=dictionary_post_values['image_path'],suplente = is_suplente )
				consejero.save()
				## In order to save a foreig key reference is nessesary pass it a instance of the object reference
				consejero_instance = Consejeros.objects.get(id =dictionary_post_values['id'] )
				## Save rfid from form and the instance , to create a link between both of them
				rfid = Rfid(id_rfid=dictionary_post_values['rfid'], id_consejero=consejero_instance)
				rfid.save()
				return HttpResponse('Asistente guardado exitosamente')
		except ValueError as v:
			print v
			return HttpResponse("Uno de los campos tiene caracteres no permitidos")
	if 'submit-form2' in request.POST:
		temp_file = request.FILES.get('fileToUpload')
		if temp_file:
			## Validate if the extension is "txt"
			ext=temp_file.name.split('.')
			ext=ext[len(ext)-1]
			if ext == "txt":
				temp_file_parse = temp_file.read().split(',')
				print 'Parsed file: ',temp_file_parse
			else:
				return HttpResponse("Formato no valido, solo se aceptan .txt")

	return render(request,'alta_template/alta_template.html')
