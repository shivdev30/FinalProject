import sys,os, subprocess, time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class Event(LoggingEventHandler):
	def on_created(self, event):
		global host
		print("Doh")
		efile=event.src_path
		print(efile)
		print("Exfil connected")
		with open (efile, "rb") as f:
			l = f.read(1024)
			while (l):
				print(l)
		#start tcp connection to send file that has been created

def exfil():
	global host
	print("In Exfil")
	print("path received")
	path= "c:\Shiv"
	observer = Observer()
	event_handler=Event()
	observer.schedule(event_handler, path, recursive=False)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	print("starting observer")
	observer.join()
	print("Observer completed")
	#s.close()
	exit(0)
	#if new file is created then send it 

def test(added):
	with open (added, 'rb') as f:
		print (f.read())
		f.close()

def test2():
	path_to_watch = "c:\Shiv"
	before = dict ([(f, None) for f in os.listdir (path_to_watch)])
	while 1:
		time.sleep (10)
		after = dict ([(f, None) for f in os.listdir (path_to_watch)])
		added = [f for f in after if not f in before]
		removed = [f for f in before if not f in after]
		if added: 
			print( "Added: ", ", ".join (added))
			test(path_to_watch + "\\" + added[0])
		if removed: print( "Removed: ", ", ".join (removed))
		before = after
test2()