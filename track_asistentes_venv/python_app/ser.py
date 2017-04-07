import serial
import time
print ("Running serial...")
rfid = 'E20051860107019126600B72'
comm = serial.Serial("COM2",115200)
while True:
	time.sleep(5)
	comm.write(rfid)
	comm.write('\r\n')
	print (rfid)