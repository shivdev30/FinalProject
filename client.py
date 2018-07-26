import sys,os
from scapy.all import *
import socket

def client(port,host):
    print ("In client")
    clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    clientsocket.connect((host,port))

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
    else : print("Nothing entered")

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
options()
