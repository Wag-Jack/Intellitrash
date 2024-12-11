"""
Server-side application for the Raspberry Pi
"""
import pickle
import socket
import time
import VL53L0X

from socket import socket, AF_INET, SOCK_STREAM

"""
TODO: FIX ConnectionResetError when disconnecting from client side
	  Set static IP for the Raspberry Pi to avoid issues with connections
"""

tof = VL53L0X.VL53L0X()

tof.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
	timing = 20000

serverPort = 3516
serverSocket = socket(AF_INET, SOCK_STREAM)
print('Socket created successfully.')

serverSocket.bind(('', serverPort))
print('Server bound to port ', serverPort)

serverSocket.listen(1)
print('Listening for incoming connections...')

print('The server is ready to receive!')	
connectionSocket, addr = serverSocket.accept()
print(f'Connection established with {addr}')
	
while True:
	data = connectionSocket.recv(4)
	
	if not data:
		break
		
	trash_height = int.from_bytes(data, byteorder='big')
	print(f'Trash can height recognized as {trash_height} mm.')
	
	#Helps to set threshold of when to alert client
	alert_threshold = trash_height * 0.1
	caution_threshold = trash_height * 0.5
	out_of_bounds = trash_height * 1.5 #when lifting the can
	
	thresholds = (alert_threshold, caution_threshold, out_of_bounds)
	send_thres = pickle.dumps(thresholds)
	connectionSocket.sendall(send_thres)
	
	#Alerts available
	sl = ['RED', 'YELLOW', 'GREEN', 'OPEN']
	status = None
	
	"""
	sensor_output = (status_flag, distance_reading)
	"""
	
	#Utilization of proximity sensor
	while True:
		distance = tof.get_distance()
	
		if distance > out_of_bounds:
			print("STOP: Trash can is currently open. Please close to continue monitoring.")
			status = sl[3]
			
			sensor_output = (status, distance)
			send_output = pickle.dumps(sensor_output)
			connectionSocket.sendall(send_output)
			
			time.sleep(3)
		
		else:
	
			if distance <= alert_threshold:
				print(f"ALERT: TRASH CAN FULL! EMPTY! ({distance} mm from sensor)")
				status = sl[0]
			elif alert_threshold < distance <= caution_threshold:
				print(f"CAUTION: Trash can over half-full. ({distance} mm from sensor)")
				status = sl[1]
			else:
				print(f"Trash is at GREAT level! ({distance} mm from sensor)")
				status = sl[2]
				
			sensor_output = (status, distance)
			send_output = pickle.dumps(sensor_output)
			connectionSocket.sendall(send_output)
		
		time.sleep(timing/1000000.00)
	
	#Code to stop sensing on server side and close connection
	tof.stop_ranging()
	connectionSocket.close()
	print('Connection closed.')
	
	"""
	(Assume a 32 gallon can with height 984.25 mm (38.75 in))
	TRASH DETECTION LEVELS:
	|TOF facing bottom |
	+-------LID--------+
	|ALERT:   5-99   mm|
	+------------------+
	|   OK: 100-499  mm|
	+------------------+
	|   			   |
	+				   +
	|GREAT: 500-1000 mm|
	+                  +
	|                  |
	+------------------+
	"""