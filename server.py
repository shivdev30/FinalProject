import sys,os
from scapy.all import *
import socket

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

options()
