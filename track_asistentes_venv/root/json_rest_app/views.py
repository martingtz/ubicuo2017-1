from django.shortcuts import render
import json
import base64
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from json_rest_app.models import Consejeros
from django.core.exceptions import ObjectDoesNotExist
from io import BytesIO
from json_rest_app.models import Consejeros
from json_rest_app.models import Rfid
from django.core.files.storage import FileSystemStorage
from django.core import serializers

# Create your views here.




## Function to respond t client with a object realted to an rfid previosly received from client
########################################################################################################################################################################
@csrf_exempt
def json_rest(request):
	## Image encoded base 64 by default in case of no one image was found
	encoded = '''
		iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAAAAACIM/FCAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxEAAAsRAX9kX5EAAARySURBVHja7dzNleMgDAfwVJcCuFOA7xTgAri7AO4U4AK4U4AL4M5dO2923r79yCRGkpd/bFRA8n4xBBkkbveTxG1ABmRABmRABmRABmRABmRABmRABmRABmRABmRATghxYc30FSVHP70jxPhE/0Rd5zeDuJW+iRrt+0BcpmeR3HtAbKJXkewbQEKlHRHQISbTvtgmaMhUaXd4YIinllhhIW2Oj+FlMCGtDnXJrZdDW6IDcUS9JSoQW1kQymiQjZgRsSCB2OGRIBPfQdUCQTYBhDYciCdRBBSIqTKI1uC6dZzpX+8nIJAqhZCDgHixQ2lZvPX8y9J8JELIpODQeSRCSNSAkO0PKSqQtTtEZWR9rCXdIUEHQnNvSFaCpN4QJYfG2LoBTBGVsSWCeDVI7AsJapCtLySrQeg0ENcVoueg5SyQcBZIHhAFiFWE0ICADa0BGZBTQvKAgEHCWSDLWSDuLLnW/TSQTQ3SN41X2vpVOd6VQWY1yNQXonBeBbH5cL8nlLkuhcwoc1189FZBpogYsqo4yr07ROd1N/aH6GTAEwBEI9/SqKyRF9VkgGVdBSJ/JBpnoRr1Wqn/IqIDsdJCJwMCkb7x6tQ19q0yVSwG7Fr3q7WGqEEkx7swNY3CV0WgKlPRsghV9/sZhjfh9Xrg1BphWBLFDiW91iSGRLPTSrFZrFmi2jGm2oe49nMoN1Q2rCdVuRdRucV12ju8snLTm37T8a4Msi7aX3tAG3invuMjGvPdc0o+pBP8mKsSbPw2H14PujPhsDsf5vWBJXlz1PcdeQvH5GP+VXOe1+AO/C4JZI6fKW+VDxb38+nlOP9/yB8jJ4oGjPntZYZ/VcdNZS5Lum7/TtGYV3UwII/+XfkJx6N7CThXdTRD/OOWkcpMAf3j/+nij4WYUHSPBr5/1y/BHAYxz28L2ZrHtn2aYtYmSgPk5aUnrcPLv/zAcADE7WmnaskG7Z7N7+K0ITv3d/fn50vV3cDbBzH7X2L3/YZuf7vcavQgbdsKr9N017Sdt2+13QVpPcrJT2e9b92VTFoQxsZujd8s9VNk7NxHHQizTKPE+a8xYebI7CSdNSBG0MZaUljcZ4SQJJ9jFCCapaQHnqK8hFiCCCuGRAxIlEJMxYC8PMN+BfEEEl4I2VAgmwxiCSasCLLgQBYRZMOBbBKIIaAwAohHgngBZEWCrAJIQYIUPsQSVFg2xGNBPBsSsSCRDclYkMyGEFhwIRMaZGJCPBrEMyERDRKZkIwGyUxIRYNUHsQQXBgWxOFBHAvi8SCeBQl4kMCCZDxIZkE2PMjGghBgcCAWEWIZEIcIcQzIgghZGJCACAkMSEKEJAYkI0IyA4LoeJL/vhmE2iEOE+KuC1kwIUszJGBCQjMkYUJSMyRjQnIzpGBCSjOEQKMVYlEhphHiUCHuqpCACglXhSRUSGqEZFRIboRsqJCtEUKwcVGIxYXYJojDhbhrQhZcyNIECbiQcE1IwoWkJkjGheRrQgoupDRBCDgGZEAG5NKQH8VLpk1SsfmeAAAAAElFTkSuQmCC
		'''
	## Variable to response the request, None by default
	response_json = None
	if request.method == "POST":
		##return HttpResponse("afafasfasfs")
		try:
			## Get json request from cliet app
			received_json =  json.loads(request.body)
			## Get rfid value from json
			rfid_from_client = received_json["rfid"]
			print 'RFID RECEIVED: ',rfid_from_client

			## Query to BD using rfid
			queryset=Consejeros.objects.get(rfid=rfid_from_client)

			try:
				## Search image related to iamge path from object and converts to 64 base
				image_path = str(queryset.image_path)
				encoded = base64.b64encode(open(image_path, "rb").read())
			except IOError:
				print 'No image found at image_path, image by default will be loaded instead'
				pass
			except TypeError:
				print 'Image file type Not valid'
				pass
			## Create a dictionary using the queryset information
			query_dic = {
					"id": str(queryset.id),
					"nombre":str(queryset.nombre),
					"facultad":str(queryset.facultad),
					"cargo":str(queryset.cargo),
					"image_encoded":encoded,
					"suplente":str(queryset.suplente),
					"fecha_inicio":str(queryset.fecha_inicio),
					}
			## Create json using the dictionary
			query_json = json.dumps(query_dic)
			response_json = query_json
		except ValueError:
			print 'Decoding JSON has failed'
			pass
		except KeyError:
			print 'Key in Json Not Found'
			pass
		except ObjectDoesNotExist,DoesNotExist:
			print 'No object related to rfid found in bd'
			pass
		except IOError:
			print 'No image found at image_path'
			pass
		except:
			print ("Something weird is happening X.X")
	## Return json to client app
	print 'sending :', response_json
	return HttpResponse(response_json)
########################################################################################################################################################################
##{% csrf_token %}
