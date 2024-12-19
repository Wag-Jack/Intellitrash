import pickle
import threading as thr
import tkinter as tk
from gui import update_trashcan_status, initialize_gui
from socket import *
from tkinter import ttk

def read_sensor_data(clientSocket, trash_height, thresholds_received, root):
    while True:
            try:
                data = clientSocket.recv(1024)
                if not data:
                    print('Connection closed by the server.')
                    break

                pi_data = pickle.loads(data)
                print(pi_data)
                root.after(0, update_trashcan_status, thresholds_received, pi_data[0], pi_data[1], trash_height)

            except TimeoutError:
                print('Receiving sensor data from server timed out.')
                break
            except OSError as e:
                print(f'Error while receiving sensor data: {str(e)}')
                break

def main():
    serverName = '192.168.0.215'
    serverPort = 8498

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.settimeout(5) #timeout after five seconds if connection stalls

    try:
        clientSocket.connect((serverName, serverPort))
        print(f'Connected to server at {serverName}:{serverPort}')
    except TimeoutError:
        print(f'Timeout occurred while trying to connect to {serverName}:{serverPort}')
        return
    except OSError as e:
        print(f'Failed to connect to server: {str(e)}')
        return

    while True:
        try:
            print('Welcome to Intellitrash!')
            trash_height = int(input('Enter height of trash can (in mm): '))
            data = trash_height.to_bytes(4, byteorder='big')
            clientSocket.send(data)

            try:
                r_data = clientSocket.recv(1024)
                thresholds_received = pickle.loads(r_data)

                root = tk.Tk()
                initialize_gui(root)
            except TimeoutError:
                print('Receiving can thresholds from server timed out.')
                return
            except OSError as e:
                print(f'Error receiving xan thresholds: {e}')
                return

            print(thresholds_received)
            
            # Main loop for receiving sensor data and updating the GUI
            sensor_thread = thr.Thread(target=read_sensor_data, args=(clientSocket, trash_height, thresholds_received, root))
            sensor_thread.start()
            root.mainloop()
                    
        except Exception as e:
            print(f'Error: {str(e)}')
            clientSocket.close()
            return
        finally:
            clientSocket.close()
            print('Client socket closed.')
        
if __name__ == '__main__':
    main()