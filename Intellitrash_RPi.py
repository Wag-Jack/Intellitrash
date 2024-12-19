import pickle
import socket
import time
import VL53L0X

from socket import socket, AF_INET, SOCK_STREAM

#Initialize the VL53L0X Time-of-Flight Distance Sensor
tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)
timing = tof.get_timing()
if (timing < 20000):
	timing = 20000

#Create TCP server socket
serverPort = 8498
serverSocket = socket(AF_INET, SOCK_STREAM)
print('Socket created successfully.')
serverSocket.bind(('', serverPort))
print('Server bound to port ', serverPort)
	
#START OF MAIN WHILE LOOP
while True:
	#Wait for incoming connections
	serverSocket.listen(1)
	print('Listening for incoming connections...')

	#Establish connection with client and begin running script
	print('The server is ready to receive!')	
	connectionSocket, addr = serverSocket.accept()
	print(f'Connection established with {addr}')
	
	try:
		
		#Try block to handle OSErrors
		try:
			#Waits for the user to send the height of the trash can from the client service
			data = connectionSocket.recv(4)
	
			if not data:
				break
		
			#Reads in the trash can height sent from the user
			trash_height = int.from_bytes(data, byteorder='big')
			print(f'Trash can height recognized as {trash_height} mm.')
	
			#Helps to set threshold of when to alert client
			alert_threshold = trash_height * 0.1
			caution_threshold = trash_height * 0.5
			out_of_bounds = trash_height * 1.5 #when lifting the can
	
			#Sends thresholds to the client
			thresholds = (alert_threshold, caution_threshold, out_of_bounds)
			send_thres = pickle.dumps(thresholds)
			connectionSocket.sendall(send_thres)
	
			#Alerts available
			sl = ['RED', 'YELLOW', 'GREEN', 'OPEN']
			status = None
		
			#try block to prevent BrokenPipeError when client closes connection
			try:	
				#Utilization of proximity sensor
				while True:
					#Get the sensor reading of the trash can
					distance = tof.get_distance()
	
					#Determines if sensor is reading while the can is open (tentatively 1.5 times trash can height)
					if distance > out_of_bounds:
						print("STOP: Trash can is currently open. Please close to continue monitoring.")
						status = sl[3]
			
						sensor_output = (status, distance)
						send_output = pickle.dumps(sensor_output)
						connectionSocket.sendall(send_output)
			
						time.sleep(3)
		
					#Sends sensor reading and current flag to set for client UI
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
		
						time.sleep(0.25)
	
				#Code to stop sensing on server side and close connection
				tof.stop_ranging()
				connectionSocket.close()
				print('Connection closed.')
		
			except BrokenPipeError:
				print("BrokenPipeError: Connection closed by client")
				connectionSocket.close()
		
		except OSError:
			print("Client reset connection")
			connectionSocket.close()
		
	except Exception as e:
		print(f'Error occurred with connection: {e}')
		connectionSocket.close()
	
#END OF MAIN WHILE LOOP
