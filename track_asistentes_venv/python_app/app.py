#!/usr/bin/env python
# -*- coding: utf-8 -*-
##E20051860107019126600B72
## Requierments:
## It's nesessary install Pillow library first -----pip install Pillow------
from Tkinter import *
import json
import urllib2
import base64
from PIL import Image,ImageTk
from io import BytesIO
import threading
import serial
import time 
import Queue

class window():
	def __init__(self,response_dict):
		## get contents of the dictionary received as a parameter
		self.id =response_dict['id']
		self.nombre =response_dict['nombre']
		self.facultad=response_dict['facultad']
		self.cargo=response_dict['cargo']
		self.image_encoded =response_dict['image_encoded']
		self.suplente=response_dict['suplente']
		self.fecha_inicio =response_dict['fecha_inicio']
		if self.suplente == '1':
			self.suplente="Si"
		else:
			self.suplente="No"
		## Child window configurations
		self.t1 = Toplevel(root)
		self.t1.geometry('%dx%d+%d+%d' % (500, 210, 0, 210* len(window_stack)))
		## Create an image object from the encoded data
		self.im = Image.open(BytesIO(base64.b64decode(self.image_encoded)))
		## Adjust size
		self.im = self.im.resize((200, 200), Image.BILINEAR)
		## Get the focus on this window
		self.t1.focus_set()
		self.t1.transient(master=root)
		self.t1.protocol("WM_DELETE_WINDOW", self.on_exit)
		Label(self.t1,padx=5, text="id",font=("Helvetica", 11),width=15,anchor = W).grid(row=0,column=0,sticky=W)
		Label(self.t1,padx=5, text="nombre",font=("Helvetica", 11),width=15,anchor = W).grid(row=1,column=0,sticky=W)
		Label(self.t1,padx=5, text="facultad",font=("Helvetica", 11),width=15,anchor = W).grid(row=2,column=0,sticky=W)
		Label(self.t1,padx=5, text="cargo",font=("Helvetica", 11),width=15,anchor = W).grid(row=3,column=0,sticky=W)
		Label(self.t1,padx=5, text="suplente",font=("Helvetica", 11),width=15,anchor = W).grid(row=4,column=0,sticky=W)
		Label(self.t1,padx=5, text="fecha de inicio",font=("Helvetica", 11),width=15,anchor = W).grid(row=5,column=0,sticky=W)
		self.photo = ImageTk.PhotoImage(image=self.im)
		Label(self.t1, image=self.photo).grid(row=0, column=2, columnspan=7, rowspan=7,sticky=W+E+N+S, padx=5, pady=5)
		self.label1=Label(self.t1, text=self.id,bg ="lightyellow",font=("Calibri", 11),width=20,anchor = W).grid(row=0,column=1,sticky=W)
		self.label1=Label(self.t1, text=self.nombre,bg ="lightyellow",font=("Calibri", 11),anchor = W,width=20).grid(row=1,column=1,sticky=W)
		self.label1=Label(self.t1, text=self.facultad,bg ="lightyellow",font=("Calibri", 11),width=20,anchor = W).grid(row=2,column=1,sticky=W)
		self.label1=Label(self.t1, text=self.cargo,bg ="lightyellow",font=("Calibri", 11),width=20,anchor = W).grid(row=3,column=1,sticky=W)
		self.label1=Label(self.t1, text=self.suplente,bg ="lightyellow",font=("Calibri", 11),width=20,anchor = W).grid(row=4,column=1,sticky=W)
		self.label1=Label(self.t1, text=self.fecha_inicio,bg ="lightyellow",font=("Calibri", 11),width=20,anchor = W).grid(row=5,column=1,sticky=W) 
	def on_exit(self):
		## Remove this window from stack
		window_stack.remove(self)
		## Destroys the window
		self.t1.destroy()




## Function to perform a request to server to get an object using rfid as key for ask
def request(RFID_to_consult):
	## Response variable
	response = None
	## URL of json rest service
	url = "http://127.0.0.1:8000/json_rest/"
	## Dectionary with rfid to ask for a object in server
	dic = {"rfid":RFID_to_consult}
	try:
		## Create a json with previous dictionary
		data = json.dumps(dic)
		## Perform the request
		r = urllib2.urlopen(url,data)
		## Read the response from server
		response = r.read()
		## Close connection
		r.close()
		## Convert the response to dictionary
		response=json.loads(response)
		print "Received from server: ",response
	except ValueError, err:
		print "Something happened! Loading JSON from server", err
		return None
	except urllib2.HTTPError, err:
		print "Something happened! Error code", err.code
		return None
	except urllib2.URLError, err:
		print "Some other error happened:", err.reason
		return None
	## Return dictionary response in other case return None
	return response


## Function to read a serial port, this function will be run in other Thread
def serial_begin(com = 'COM3'):
	## Flag to maintain loop running
	recibido = False
	try:
		print ("Running serial...")
		## Open serial port
		comm = serial.Serial("COM3",115200)
		## Enable flag
		read = True
		#Main loop
		while read:
			## Verify if is nessesary keep running serial port thread
			try:
				## Get flag
				item = q.get(False)
				if item == 'stop':
					print ("Stopping serial")
					## Exit Thread
					return None  # or return
			except Queue.Empty:
				pass
			#Check Buffer Data
			try:
				while comm.inWaiting() >0:
					#Read the Data
					data = comm.readline()
					## Flag to know if something was received
					recibido=True
					if recibido: 
						print 'leido: ',data
						print ""
						## Clean the data read from newlines and carriage return
						data = data.strip('\r\n')
						## Put the data readed in the queue
						rfid_queue.put(data)
						## Disables the flag
						recibido = False
					## Clean the data variable
					data = ""
			except IOError:
				print "Port is disconected"
				read = False
				pass
	except Exception:
		print "Error opening port"
		pass

## Function to send stop signal to serial read Thread
def stop():
    q.put('stop')
## Funtion to start/stop read serial port Thread 
def start_thread():
	## Reference to Thread variable
	global t
	## Verify if Thread is running
	if t.isAlive() == True:
		stop()
	else:
		t = threading.Thread(target=serial_begin)
		t.start()
## Function to admin child windows
def window_manager():
	## Reference to lock object
	global window_lock
	try:
		if (len(window_stack) == 0):
			window_lock = False
		if len(window_stack) == 3:
			window_lock = True
			##print ("Maximas ventanas permitidas")
		if window_lock == False:
			## Get rfid from queue
			rfid = rfid_queue.get(False)
			## Call request function with the rfid from queue
			response_dict=request(rfid)
			if response_dict:
				## Add new window to stack
				window_stack.append(window(response_dict))
	except Queue.Empty:
		pass

def check_request():
	##print "Cola size: ",rfid_queue.qsize()
	if not rfid_queue.empty():
		window_manager()
	root.after(300,check_request)

## Function to update labels
def callback1():
	global t
	queue_label_size.config(text=rfid_queue.qsize())
	if t.isAlive() == True:
		serial_button.config(text='Stop',bg='green')
	else:
		serial_button.config(text='Start',bg='red')

	root.after(300,callback1)

## Function that executes when push X button in window
def on_exit():
	## Stop serial port thread
	stop()
	## Destroys the window
	root.destroy()

## App
## Variable to control acces to a variable between diferents Threads
window_lock = False
## queue to control start/stop of serial port Thread
q = Queue.Queue()
## queue to save rfids readed from serial port
rfid_queue = Queue.Queue()
## Thread serial port
t = threading.Thread(target=serial_begin)
## Stack of child windows 
window_stack = []
## Main window
root = Tk()
## Window size and title
root.title("Main window")
root.geometry('200x200')
## Links on_exit() function to X button in window
root.protocol("WM_DELETE_WINDOW", on_exit)
## Button to start/stop serial Thread communication
serial_button = Button(root, font=("Helvetica", 11),text="Start",command=start_thread)
serial_button.pack(pady=5)
## Label
queue_label = Label(root, text="Elementos en la cola:",font=("Helvetica", 11))
queue_label.pack(pady=5)
## Label with the size of the rfid queue
queue_label_size = Label(root, text="0",font=("Helvetica", 11))
queue_label_size.pack(pady=5)
## Functions that executes every x time
## Check if the rfid has something and display window
root.after(300,check_request)
## updting labels
root.after(300,callback1)
## Keep GUI running
root.mainloop()