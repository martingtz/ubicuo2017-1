def get_form_data(request,dict_types):
	## Check if is a POST request
	if request.method == "POST":
		## extensions admited for images
		image_ext =['jpg','png']
		## Check from what form comes the request
		if 'submit-form1' in request.POST:
			# Store all request POST fields in a dictionary
			dictionary_post_values = {}
			dictionary_post_values['id'] = request.POST['id'];
			dictionary_post_values['nombre'] = request.POST['name'];
			dictionary_post_values['facultad'] = request.POST['facultad'];
			dictionary_post_values['cargo'] = request.POST['cargo'];
			dictionary_post_values['suplente'] = request.POST['suplente'];
			dictionary_post_values['image_path'] = request.POST['imagen'];
			## Validate if exists empty fields
			for item in dictionary_post_values:
				if item == "":
					return HttpResponse("Hay campos vacios")
			## Save the image in object media file
			image_uploaded = request.FILES.get('imagen')
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
			if dictionary_post_values['facultad'] == 'no':
				is_suplente = False
			assistants=Consejeros(id =dictionary_post_values['id'], nombre =dictionary_post_values['nombre'],facultad=dictionary_post_values['facultad'],cargo=dictionary_post_values['cargo'],image_path=dictionary_post_values['image_path'],suplente = is_suplente )
			assistants.save()

